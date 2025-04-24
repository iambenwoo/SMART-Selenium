from selenium.webdriver.common.by import By
from .utils import get_timestamp, clear_and_enter_text, wait_and_click, wait_for_disappear, NumPad
import time


class XPath:
    # Locator constants
    ION_BACKDROP_SELECTOR = "ion-backdrop.sc-ion-loading-ios.ios.backdrop-no-tappable.hydrated"
    FNA_START_NEW_BUTTON = "(.//*[normalize-space(text()) and normalize-space(.)='財務需要分析'])[2]/following::button[1]"
    FAMILY_NAME_INPUT = "//div[@id='familyName']/div[2]/ion-input/input"
    GIVEN_NAME_INPUT = "//div[@id='givenName']/div[2]/ion-input/input"
    MOBILE_NUMBER_INPUT = "//div[@id='mobile']/div[2]/ion-input/input"
    NUMBER_OF_DEPENDENT_SELECT = "(.//*[normalize-space(text()) and normalize-space(.)='受養人數目'])[1]/following::ion-select[1]"
    NUMBER_OF_DEPENDENT = "//ion-popover[@id='ion-overlay-{seq}']/div/div[2]/ion-select-popover/ion-list/ion-radio-group/ion-item{option}/ion-radio"
    MARITAL_STATUS_SELECT = "(.//*[normalize-space(text()) and normalize-space(.)='婚姻狀況'])[1]/following::ion-select[1]"
    MARITAL_STATUS = "//ion-popover[@id='ion-overlay-{seq}']/div/div[2]/ion-select-popover/ion-list/ion-radio-group/ion-item{option}/ion-radio"
    OCCUPATION_SELECT = "(.//*[normalize-space(text()) and normalize-space(.)='職業'])[1]/following::div[4]"
    OCCUPATION_SELECT_EDUCATION = "//*/text()[normalize-space(.)='教育']/parent::*"
    OCCUPATION_SELECT_EDUCATION_PRINCIPLE = "//*/text()[normalize-space(.)='校長']/parent::*"
    EDUCATION_LEVEL_SELECT = "(.//*[normalize-space(text()) and normalize-space(.)='教育程度'])[1]/following::ion-select[1]"
    EDUCATION_LEVEL = "//ion-popover[@id='ion-overlay-{seq}']/div/div[2]/ion-select-popover/ion-list/ion-radio-group/ion-item{option}/ion-radio"
    RETIREMENT_AGE_SELECT = "//div[@id='retirementAge']/div[2]/div/span"
    ANB_SELECT = "(.//*[normalize-space(text()) and normalize-space(.)='出生日期 (下次生日年齡)'])[1]/following::span[2]"
    ANB_YEAR_SELECT = "//ion-modal[@id='ion-overlay-{seq}']/div/li-ionic4-datepicker-modal/ion-content/ion-grid/ion-row/ion-col[2]/ion-grid/ion-row/ion-col[3]/ion-button"
    ANB_YEAR_VALUE = "//*/text()[normalize-space(.)='1997']/parent::*"
    ANB_MONTH_SELECT = "//ion-modal[@id='ion-overlay-{seq}']/div/li-ionic4-datepicker-modal/ion-content/ion-grid/ion-row/ion-col[2]/ion-grid/ion-row/ion-col/ion-button"
    ANB_MONTH_VALUE = "//*/text()[normalize-space(.)='七月']/parent::*"
    ANB_DAY_VALUE = "//*/text()[normalize-space(.)='10']/parent::*"
    ANB_CONFIRM = "//ion-modal[@id='ion-overlay-{seq}']/div/li-ionic4-datepicker-modal/ion-footer/ion-toolbar/ion-grid/ion-row/ion-col[3]/ion-button"
    EXTRA_LIFE_SELECT = "//div[@id='extraLifeProtNeeds']/div[2]/div"
    EXTRA_MEDICAL_SELECT = "//div[@id='extMedCrisisBeneNeeds']/div[2]/div"
    EXTRA_SAVING_SELECT = "//div[@id='extReqNetSaving']/div[2]/div"


class Column:
    # Column constants
    FAMILY_NAME_ENG = "Family_Name_ENG"
    GIVEN_NAME_ENG = "Given_Name_ENG"
    MOBILE_NUMBER = "Mobile_Number"
    MARITAL_STATUS = "Marital_Status"
    NUMBER_OF_DEPENDENTS = "Number_of_Dependents"
    OCCUPATION_SELECT = "Occupation_Select"
    EDUCATION_LEVEL = "Education_Level"
    RETIREMENT_AGE = "Retirement_Age"
    EXTRA_LIFE = "Extra_Life"
    EXTRA_MEDICAL = "Extra_Medical"
    EXTRA_SAVING = "Extra_Saving"


class FNAHelpers:

    @staticmethod
    def input_english_name(driver, map):
        try:
            clear_and_enter_text(
                driver, XPath.FAMILY_NAME_INPUT, map.get(Column.FAMILY_NAME_ENG, ""))
            clear_and_enter_text(
                driver, XPath.GIVEN_NAME_INPUT, map.get(Column.GIVEN_NAME_ENG, ""))
        except Exception as e:
            print(f"ERROR: Failed to input names - {str(e)}")
            raise

    @staticmethod
    def input_mobile_number(driver, map):
        try:
            clear_and_enter_text(
                driver, XPath.MOBILE_NUMBER_INPUT, map.get(Column.MOBILE_NUMBER, ""))
        except Exception as e:
            print(f"ERROR: Failed to input mobile number - {str(e)}")
            raise

    @staticmethod
    def set_marital_status(driver, map, overlay_seq):
        try:
            marital_status = map.get(Column.MARITAL_STATUS)
            wait_and_click(driver, XPath.MARITAL_STATUS_SELECT)
            time.sleep(1)
            wait_and_click(driver, XPath.MARITAL_STATUS_SELECT)

            marital_status_options = {
                "single": "",
                "married": "[2]",
                "divorced": "[3]",
                "widowed": "[4]",
            }

            if marital_status not in marital_status_options:
                raise ValueError(f"Invalid marital status: {marital_status}")

            wait_and_click(driver, XPath.MARITAL_STATUS.format(
                seq=overlay_seq, option=marital_status_options[marital_status]))
            time.sleep(1)
        except Exception as e:
            print(f"ERROR: Failed to set marital status - {str(e)}")
            raise

    @staticmethod
    def set_number_of_dependents(driver, map, overlay_seq):
        try:
            number_of_dependents = map.get(Column.NUMBER_OF_DEPENDENTS)
            wait_and_click(driver, XPath.NUMBER_OF_DEPENDENT_SELECT)
            time.sleep(1)
            wait_and_click(driver, XPath.NUMBER_OF_DEPENDENT_SELECT)

            number_of_dependents_options = {
                "nil": "",
                "1-3": "[2]",
                "4-6": "[3]",
                "7-above": "[4]",
            }

            if number_of_dependents not in number_of_dependents_options:
                raise ValueError(
                    f"Invalid number of dependents: {number_of_dependents}")

            wait_and_click(driver, XPath.NUMBER_OF_DEPENDENT.format(
                seq=overlay_seq, option=number_of_dependents_options[number_of_dependents]))
            time.sleep(1)
        except Exception as e:
            print(f"ERROR: Failed to set number of dependents - {str(e)}")
            raise

    @staticmethod
    def start_new_fna(driver):
        try:
            wait_for_disappear(
                driver, XPath.ION_BACKDROP_SELECTOR, By.CSS_SELECTOR)
            time.sleep(10)
            wait_and_click(driver, XPath.FNA_START_NEW_BUTTON)
        except Exception as e:
            print(f"ERROR: Failed to start new FNA - {str(e)}")
            raise

    @staticmethod
    def set_occupation(driver, map):
        try:
            # occupation = map.get(Column.OCCUPATION_SELECT)
            wait_and_click(driver, XPath.OCCUPATION_SELECT)
            time.sleep(2)
            wait_and_click(driver, XPath.OCCUPATION_SELECT_EDUCATION)
            time.sleep(2)
            wait_and_click(driver, XPath.OCCUPATION_SELECT_EDUCATION_PRINCIPLE)
        except Exception as e:
            print(f"ERROR: Failed to select occupation - {str(e)}")
            raise

    @staticmethod
    def set_education_level(driver, map, overlay_seq):
        try:
            education_level = map.get(Column.EDUCATION_LEVEL)
            wait_and_click(driver, XPath.EDUCATION_LEVEL_SELECT)
            time.sleep(1)
            wait_and_click(driver, XPath.EDUCATION_LEVEL_SELECT)

            education_level_options = {
                "primary": "",
                "secondary": "[2]",
                "vocational": "[3]",
                "university": "[4]",
            }

            if education_level not in education_level_options:
                raise ValueError(f"Invalid education level: {education_level}")

            wait_and_click(driver, XPath.EDUCATION_LEVEL.format(
                seq=overlay_seq, option=education_level_options[education_level]))
            time.sleep(1)
        except Exception as e:
            print(f"ERROR: Failed to select education - {str(e)}")
            raise

    @staticmethod
    def set_retirement_age_num_pad(driver, map, overlay_seq, num_pad_seq):
        try:
            retirement_age = map.get(Column.RETIREMENT_AGE)
            wait_and_click(driver, XPath.RETIREMENT_AGE_SELECT)
            time.sleep(1)
            wait_and_click(driver, XPath.RETIREMENT_AGE_SELECT)

            NumPad.wait_and_click(driver, overlay_seq, num_pad_seq, retirement_age)
        except Exception as e:
            print(f"ERROR: Failed to set retirement age - {str(e)}")
            raise

    @staticmethod
    def set_anb(driver, map, overlay_seq):
        try:
            wait_and_click(driver, XPath.ANB_SELECT)
            time.sleep(1)
            wait_and_click(driver, XPath.ANB_SELECT)
            time.sleep(1)
            wait_and_click(
                driver, XPath.ANB_YEAR_SELECT.format(seq=overlay_seq))
            wait_and_click(driver, XPath.ANB_YEAR_VALUE)
            wait_and_click(
                driver, XPath.ANB_MONTH_SELECT.format(seq=overlay_seq))
            wait_and_click(driver, XPath.ANB_MONTH_VALUE)
            wait_and_click(driver, XPath.ANB_DAY_VALUE)
            wait_and_click(driver, XPath.ANB_CONFIRM.format(seq=overlay_seq))
        except Exception as e:
            print(f"ERROR: Failed to set ANB - {str(e)}")
            raise

    @staticmethod
    def set_extra_life(driver, map, overlay_seq, num_pad_seq):
        try:
            extra_life = map.get(Column.EXTRA_LIFE)
            wait_and_click(driver, XPath.EXTRA_LIFE_SELECT)
            time.sleep(1)
            wait_and_click(driver, XPath.EXTRA_LIFE_SELECT)        

            NumPad.wait_and_click(driver, overlay_seq, num_pad_seq, extra_life)
        except Exception as e:
            print(f"ERROR: Failed to set extra life - {str(e)}")
            raise

    @staticmethod
    def set_extra_medical(driver, map, overlay_seq, num_pad_seq):
        try:
            extra_medical = map.get(Column.EXTRA_MEDICAL)
            wait_and_click(driver, XPath.EXTRA_MEDICAL_SELECT)
            NumPad.wait_and_click(driver, overlay_seq, num_pad_seq, extra_medical)
        except Exception as e:
            print(f"ERROR: Failed to set extra medical - {str(e)}")
            raise

    @staticmethod
    def set_extra_saving(driver, map, overlay_seq, num_pad_seq):
        try:
            extra_saving = map.get(Column.EXTRA_SAVING)
            wait_and_click(driver, XPath.EXTRA_SAVING_SELECT)
            time.sleep(1)
            wait_and_click(driver, XPath.EXTRA_SAVING_SELECT)
            NumPad.wait_and_click(driver, overlay_seq, num_pad_seq, extra_saving)
        except Exception as e:
            print(f"ERROR: Failed to set extra saving - {str(e)}")
            raise
