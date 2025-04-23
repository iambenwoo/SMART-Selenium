from selenium.webdriver.common.by import By
from .utils import get_timestamp, clear_and_enter_text, wait_and_click, wait_for_disappear
import time


class XPath:
    # Locator constants
    ION_BACKDROP_SELECTOR = "ion-backdrop.sc-ion-loading-ios.ios.backdrop-no-tappable.hydrated"
    FNA_START_NEW_BUTTON = "(.//*[normalize-space(text()) and normalize-space(.)='財務需要分析'])[2]/following::button[1]"
    FAMILY_NAME_INPUT = "//div[@id='familyName']/div[2]/ion-input/input"
    GIVEN_NAME_INPUT = "//div[@id='givenName']/div[2]/ion-input/input"
    MOBILE_NUMBER_INPUT = "//div[@id='mobile']/div[2]/ion-input/input"
    NUMBER_OF_DEPENDENT_SELECT = "(.//*[normalize-space(text()) and normalize-space(.)='受養人數目'])[1]/following::ion-select[1]"
    NUMBER_OF_DEPENDENT_NIL = "//ion-popover[@id='ion-overlay-4']/div/div[2]/ion-select-popover/ion-list/ion-radio-group/ion-item/ion-radio"
    NUMBER_OF_DEPENDENT_1_3 = "//ion-popover[@id='ion-overlay-4']/div/div[2]/ion-select-popover/ion-list/ion-radio-group/ion-item[2]/ion-radio"
    NUMBER_OF_DEPENDENT_4_6 = "//ion-popover[@id='ion-overlay-4']/div/div[2]/ion-select-popover/ion-list/ion-radio-group/ion-item[3]/ion-radio"
    NUMBER_OF_DEPENDENT_7_ABOVE = "//ion-popover[@id='ion-overlay-4']/div/div[2]/ion-select-popover/ion-list/ion-radio-group/ion-item[4]/ion-radio"
    MARITAL_STATUS_SELECT = "(.//*[normalize-space(text()) and normalize-space(.)='婚姻狀況'])[1]/following::ion-select[1]"
    MARITAL_STATUS_SINGLE = "//ion-popover[@id='ion-overlay-3']/div/div[2]/ion-select-popover/ion-list/ion-radio-group/ion-item/ion-radio"
    MARITAL_STATUS_MARRIED = "//ion-popover[@id='ion-overlay-3']/div/div[2]/ion-select-popover/ion-list/ion-radio-group/ion-item[2]/ion-radio"
    MARITAL_STATUS_DIVORCED = "//ion-popover[@id='ion-overlay-3']/div/div[2]/ion-select-popover/ion-list/ion-radio-group/ion-item[3]/ion-radio"
    MARITAL_STATUS_WIDOWED = "//ion-popover[@id='ion-overlay-3']/div/div[2]/ion-select-popover/ion-list/ion-radio-group/ion-item[4]/ion-radio"
    OCCUPATION_SELECT = "(.//*[normalize-space(text()) and normalize-space(.)='職業'])[1]/following::div[4]"
    OCCUPATION_SELECT_EDUCATION = "//*/text()[normalize-space(.)='教育']/parent::*"
    OCCUPATION_SELECT_EDUCATION_PRINCIPLE = "//*/text()[normalize-space(.)='校長']/parent::*"
    EDUCATION_SELECT = "(.//*[normalize-space(text()) and normalize-space(.)='教育程度'])[1]/following::ion-select[1]"
    EDUCATION_SELECT_PRIMARY = "//ion-popover[@id='ion-overlay-5']/div/div[2]/ion-select-popover/ion-list/ion-radio-group/ion-item/ion-radio"
    EDUCATION_SELECT_SECONDARY = "//ion-popover[@id='ion-overlay-5']/div/div[2]/ion-select-popover/ion-list/ion-radio-group/ion-item[2]/ion-radio"
    EDUCATION_SELECT_VOCATIONAL = "//ion-popover[@id='ion-overlay-5']/div/div[2]/ion-select-popover/ion-list/ion-radio-group/ion-item[3]/ion-radio"
    EDUCATION_SELECT_UNIVERSITY = "//ion-popover[@id='ion-overlay-5']/div/div[2]/ion-select-popover/ion-list/ion-radio-group/ion-item[4]/ion-radio"

class Column:
    # Column constants
    FAMILY_NAME_ENG = "Family_Name_ENG"
    GIVEN_NAME_ENG = "Given_Name_ENG"
    MOBILE_NUMBER = "Mobile_Number"
    MARITAL_STATUS = "Marital_Status"
    NUMBER_OF_DEPENDENTS = "Number_of_Dependents"

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
    def set_marital_status(driver, map):
        try:
            marital_status = map.get(Column.MARITAL_STATUS)
            wait_and_click(driver, XPath.MARITAL_STATUS_SELECT)
            time.sleep(1)
            wait_and_click(driver, XPath.MARITAL_STATUS_SELECT)

            marital_status_options = {
                "single": XPath.MARITAL_STATUS_SINGLE,
                "married": XPath.MARITAL_STATUS_MARRIED,
                "divorced": XPath.MARITAL_STATUS_DIVORCED,
                "widowed": XPath.MARITAL_STATUS_WIDOWED,
            }

            if marital_status not in marital_status_options:
                raise ValueError(f"Invalid marital status: {marital_status}")

            wait_and_click(driver, marital_status_options[marital_status])
            time.sleep(1)
        except Exception as e:
            print(f"ERROR: Failed to set marital status - {str(e)}")
            raise

    @staticmethod
    def set_number_of_dependents(driver, map):
        try:
            number_of_dependents = map.get(Column.NUMBER_OF_DEPENDENTS)
            wait_and_click(driver, XPath.NUMBER_OF_DEPENDENT_SELECT)

            dependent_options = {
                "nil": XPath.NUMBER_OF_DEPENDENT_NIL,
                "1-3": XPath.NUMBER_OF_DEPENDENT_1_3,
                "4-6": XPath.NUMBER_OF_DEPENDENT_4_6,
                "7-above": XPath.NUMBER_OF_DEPENDENT_7_ABOVE,
            }

            if number_of_dependents not in dependent_options:
                raise ValueError(
                    f"Invalid number of dependents: {number_of_dependents}")

            wait_and_click(driver, dependent_options[number_of_dependents])
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
            #occupation = map.get(Column.OCCUPATION_SELECT)
            wait_and_click(driver, XPath.OCCUPATION_SELECT)
            time.sleep(2)
            wait_and_click(driver, XPath.OCCUPATION_SELECT_EDUCATION)
            time.sleep(2)
            wait_and_click(driver, XPath.OCCUPATION_SELECT_EDUCATION_PRINCIPLE)
        except Exception as e:
            print(f"ERROR: Failed to select occupation - {str(e)}")
            raise

    @staticmethod
    def set_education(driver, map):
        try:
            education_level = map.get("Education_Level")
            wait_and_click(driver, XPath.EDUCATION_SELECT)
            time.sleep(1)
            wait_and_click(driver, XPath.EDUCATION_SELECT)

            education_options = {
                "primary": XPath.EDUCATION_SELECT_PRIMARY,
                "secondary": XPath.EDUCATION_SELECT_SECONDARY,
                "vocational": XPath.EDUCATION_SELECT_VOCATIONAL,
                "university": XPath.EDUCATION_SELECT_UNIVERSITY,
            }

            if education_level not in education_options:
                raise ValueError(f"Invalid education level: {education_level}")

            wait_and_click(driver, education_options[education_level])
            time.sleep(1)
        except Exception as e:
            print(f"ERROR: Failed to select education - {str(e)}")
            raise