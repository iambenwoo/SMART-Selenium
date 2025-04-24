from .utils import teardown_driver
from .login import Login
from .fna_helper import FNAHelpers

class FNA:
    def perform_fna(self, map):
        driver = Login.perform_login(map)
        overlay_seq = 2
        num_pad_seq = 2

        try:
            # Start new FNA
            FNAHelpers.start_new_fna(driver)

            # Set retirement age
            overlay_seq += 1
            num_pad_seq = 3
            FNAHelpers.set_retirement_age_num_pad(driver, map, overlay_seq, num_pad_seq)

            overlay_seq += 1
            num_pad_seq = 2
            FNAHelpers.set_extra_saving(driver, map, overlay_seq, num_pad_seq)

            overlay_seq += 1
            num_pad_seq = 2
            FNAHelpers.set_extra_life(driver, map, overlay_seq, num_pad_seq)

            overlay_seq += 1
            num_pad_seq = 2
            FNAHelpers.set_extra_medical(driver, map, overlay_seq, num_pad_seq)
        
            # Set marital status
            overlay_seq += 1
            FNAHelpers.set_marital_status(driver, map, overlay_seq)

            # Set education level
            overlay_seq += 1
            FNAHelpers.set_education_level(driver, map, overlay_seq)

            # Set number of dependents
            overlay_seq += 1
            FNAHelpers.set_number_of_dependents(driver, map, overlay_seq)

            # Set occupation
            FNAHelpers.set_occupation(driver, map)

            
            # Set ANB
            overlay_seq += 1
            FNAHelpers.set_anb(driver, map, overlay_seq)



            # Input English name and mobile number
            FNAHelpers.input_english_name(driver, map)
            # FNAHelpers.input_mobile_number(driver, map)  # Uncomment if needed

        except Exception as e:
            print(f"ERROR: {str(e)}")
            raise
        finally:
            teardown_driver(driver)
