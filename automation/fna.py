from .utils import teardown_driver
from .login import Login
from .fna_helper import FNAHelpers


class FNA:

    def perform_fna(self, map):
        driver = Login.perform_login(map)

        try:
            FNAHelpers.start_new_fna(driver)
            FNAHelpers.set_marital_status(driver, map)
            FNAHelpers.set_number_of_dependents(driver, map)
            FNAHelpers.set_occupation(driver, map)
            FNAHelpers.set_education_level(driver, map)
            FNAHelpers.set_retirement_age(driver, map)
            FNAHelpers.set_anb(driver, map)
            FNAHelpers.input_english_name(driver, map)
            # Uncomment the line below if mobile number input is required
            # FNAHelpers.input_mobile_number(driver, map)
        except Exception as e:
            print(f"ERROR: {str(e)}")
            raise
        finally:
            teardown_driver(driver)
