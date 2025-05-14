from .utils import teardown_driver
from .login import Login
from .fna_helper import FNAHelpers

class FNAStep:
    def __init__(self, method, requires_overlay=True, num_pad_seq=None):
        self.method = method
        self.requires_overlay = requires_overlay
        self.num_pad_seq = num_pad_seq

class FNA:
    FNA_STEPS = [
        FNAStep(FNAHelpers.start_new_fna, requires_overlay=False),
        #FNAStep(FNAHelpers.set_retirement_age, num_pad_seq=3),
        #FNAStep(FNAHelpers.set_extra_saving, num_pad_seq=2),
        #FNAStep(FNAHelpers.set_extra_life, num_pad_seq=2),
        #FNAStep(FNAHelpers.set_extra_medical, num_pad_seq=2),
        #FNAStep(FNAHelpers.set_time_to_achieve, num_pad_seq=2),
        #FNAStep(FNAHelpers.set_objective, requires_overlay=False),
        #FNAStep(FNAHelpers.set_target_period, requires_overlay=False),  
        #FNAStep(FNAHelpers.set_income_source, requires_overlay=False),
        #FNAStep(FNAHelpers.set_monthly_prem_expense, num_pad_seq=2),
        # FNAStep(FNAHelpers.set_monthly_disposable_income, num_pad_seq=2),
        # FNAStep(FNAHelpers.set_payment_income_ratio, requires_overlay=False),
        # FNAStep(FNAHelpers.set_payment_period, requires_overlay=False),
        FNAStep(FNAHelpers.set_assets, requires_overlay=False),
        #FNAStep(FNAHelpers.set_marital_status),
        #FNAStep(FNAHelpers.set_education_level),
        #FNAStep(FNAHelpers.set_number_of_dependents),
        #FNAStep(FNAHelpers.set_occupation, requires_overlay=False),
        #FNAStep(FNAHelpers.set_anb),
        #FNAStep(FNAHelpers.input_english_name, requires_overlay=False),
    ]

    def perform_fna(self, map):
        driver = Login.perform_login(map)
        overlay_seq = 3

        try:
            for step in self.FNA_STEPS:
                if step.requires_overlay:
                    if step.num_pad_seq:
                        step.method(driver, map, overlay_seq, step.num_pad_seq)
                    else:
                        step.method(driver, map, overlay_seq)
                    overlay_seq += 1
                else:
                    step.method(driver, map)
                    
        except Exception as e:
            print(f"ERROR: {str(e)}")
            raise
        finally:
            teardown_driver(driver)