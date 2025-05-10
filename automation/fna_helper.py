from selenium.webdriver.common.by import By
from .utils import get_timestamp, input_text, click, click_by_CSS, wait_for_disappear, NumPad
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC


class XPath:
    # Locator constants
    ION_BACKDROP_SELECTOR = "ion-backdrop.sc-ion-loading-ios.ios.backdrop-no-tappable.hydrated"
    FNA_START_NEW_BUTTON = "(.//*[normalize-space(text()) and normalize-space(.)='財務需要分析'])[2]/following::button[1]"
    FAMILY_NAME_ENG_INPUT = "//div[@id='familyName']/div[2]/ion-input/input"
    GIVEN_NAME_ENG_INPUT = "//div[@id='givenName']/div[2]/ion-input/input"
    MOBILE_NUMBER_INPUT = "//div[@id='mobile']/div[2]/ion-input/input"
    NUMBER_OF_DEPENDENT_SELECT = "(.//*[normalize-space(text()) and normalize-space(.)='受養人數目'])[1]/following::ion-select[1]"
    NUMBER_OF_DEPENDENT = "//ion-popover[@id='ion-overlay-{seq}']/div/div[2]/ion-select-popover/ion-list/ion-radio-group/ion-item{option}/ion-radio"
    MARITAL_STATUS_SELECT = "(.//*[normalize-space(text()) and normalize-space(.)='婚姻狀況'])[1]/following::ion-select[1]"
    MARITAL_STATUS_OPTION = "//ion-popover[@id='ion-overlay-{seq}']/div/div[2]/ion-select-popover/ion-list/ion-radio-group/ion-item{option}/ion-radio"
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
    TIME_TO_ACHIEVE_SELECT = "//div[@id='timeToAchieveSavingAmt']/div[2]/div"
    OBJECTIVE_SELECT = "ion-list ion-item ion-checkbox"
    TARGET_PERIOD = "ion-radio-group ion-item ion-radio"
    MONTHLY_PREM_EXPENSE = "//div[@id='monthlyPremExpense']/div[2]/div"
    MONTHLY_DISPOSABLE_INCOME = "//div[@id='monthlyDispIncomeAmt']/div[2]/div"

class Column:
    # Column constants
    FAMILY_NAME_ENG = "Family_Name_ENG"
    GIVEN_NAME_ENG = "Given_Name_ENG"
    MOBILE_NUMBER = "Mobile_Number"
    MARITAL_STATUS = "Marital_Status"
    NUMBER_OF_DEPENDENTS = "Number_of_Dependents"
    EDUCATION_LEVEL = "Education_Level"
    RETIREMENT_AGE = "Retirement_Age"
    EXTRA_LIFE = "Extra_Life"
    EXTRA_MEDICAL = "Extra_Medical"
    EXTRA_SAVING = "Extra_Saving"
    TIME_TO_ACHIEVE = "Time_to_Achieve"
    OBJECTIVE = "Objective"
    TARGET_PERIOD = "Target_Period"
    MONTHLY_PREM_EXPENSE = "Monthly_Prem_Expense"
    MONTHLY_DISPOSABLE_INCOME = "Monthly_Disposable_Income"


class OptionConstants:
    MARITAL_STATUS_OPTIONS = {
        "single": "",
        "married": "[2]",
        "divorced": "[3]",
        "widowed": "[4]",
    }

    NUMBER_OF_DEPENDENTS_OPTIONS = {
        "nil": "",
        "1-3": "[2]",
        "4-6": "[3]",
        "7-above": "[4]",
    }

    EDUCATION_LEVEL_OPTIONS = {
        "primary": "",
        "secondary": "[2]",
        "vocational": "[3]",
        "university": "[4]",
    }

    OBJECTIVE_OPTIONS = {
        "a": 0,
        "b": 1,
        "c": 2,
        "d": 3,
        "e": 4,
        "f": 5,
    }

    TARGET_PERIOD_OPTIONS = {
        "a": 0,
        "b": 1,
        "c": 2,
        "d": 3,
        "e": 4,
        "f": 5,
        "g": 6,
    }


class FNAHelpers:

    @staticmethod
    def input_english_name(driver, map):
        try:
            value = map.get(Column.FAMILY_NAME_ENG, "")
            xpath = XPath.FAMILY_NAME_ENG_INPUT
            input_text(driver, xpath, value)

            value = map.get(Column.GIVEN_NAME_ENG, "")
            xpath = XPath.GIVEN_NAME_ENG_INPUT
            input_text(driver, xpath, value)
        except Exception as e:
            print(f"ERROR: Failed to input names - {str(e)}")
            raise

    @staticmethod
    def input_mobile_number(driver, map):
        try:
            value = map.get(Column.MOBILE_NUMBER, "")
            xpath = XPath.MOBILE_NUMBER_INPUT
            input_text(driver, xpath, value)
        except Exception as e:
            print(f"ERROR: Failed to input mobile number - {str(e)}")
            raise

    @staticmethod
    def set_marital_status(driver, map, overlay_seq):
        try:
            value = map.get(Column.MARITAL_STATUS)
            xpath = XPath.MARITAL_STATUS_SELECT
            click(driver, xpath)
            time.sleep(1)
            click(driver, xpath)

            options = OptionConstants.MARITAL_STATUS_OPTIONS
            if value not in options:
                raise ValueError(f"Invalid marital status: {value}")

            xpath = XPath.MARITAL_STATUS_OPTION.format(
                seq=overlay_seq, option=options[value])
            click(driver, xpath)
            time.sleep(1)
        except Exception as e:
            print(f"ERROR: Failed to set marital status - {str(e)}")
            raise

    @staticmethod
    def set_number_of_dependents(driver, map, overlay_seq):
        try:
            value = map.get(Column.NUMBER_OF_DEPENDENTS)
            xpath = XPath.NUMBER_OF_DEPENDENT_SELECT
            click(driver, xpath)
            time.sleep(1)
            click(driver, xpath)

            options = OptionConstants.NUMBER_OF_DEPENDENTS_OPTIONS
            if value not in options:
                raise ValueError(
                    f"Invalid number of dependents: {value}")

            xpath = XPath.NUMBER_OF_DEPENDENT.format(
                seq=overlay_seq, option=options[value])
            click(driver, xpath)
            time.sleep(1)
        except Exception as e:
            print(f"ERROR: Failed to set number of dependents - {str(e)}")
            raise

    @staticmethod
    def start_new_fna(driver, map):
        try:
            wait_for_disappear(
                driver, XPath.ION_BACKDROP_SELECTOR, By.CSS_SELECTOR)
            time.sleep(12)
            click(driver, XPath.FNA_START_NEW_BUTTON)
        except Exception as e:
            print(f"ERROR: Failed to start new FNA - {str(e)}")
            raise

    @staticmethod
    def set_occupation(driver, map):
        try:
            xpath = XPath.OCCUPATION_SELECT
            click(driver, xpath)
            time.sleep(2)
            xpath = XPath.OCCUPATION_SELECT_EDUCATION
            click(driver, xpath)
            time.sleep(2)
            xpath = XPath.OCCUPATION_SELECT_EDUCATION_PRINCIPLE
            click(driver, xpath)
        except Exception as e:
            print(f"ERROR: Failed to select occupation - {str(e)}")
            raise

    @staticmethod
    def set_education_level(driver, map, overlay_seq):
        try:
            value = map.get(Column.EDUCATION_LEVEL)
            xpath = XPath.EDUCATION_LEVEL_SELECT
            click(driver, xpath)
            time.sleep(1)
            click(driver, xpath)

            options = OptionConstants.EDUCATION_LEVEL_OPTIONS
            if value not in options:
                raise ValueError(f"Invalid education level: {value}")

            xpath = XPath.EDUCATION_LEVEL.format(
                seq=overlay_seq, option=options[value])
            click(driver, xpath)
            time.sleep(1)
        except Exception as e:
            print(f"ERROR: Failed to select education - {str(e)}")
            raise

    @staticmethod
    def set_retirement_age(driver, map, overlay_seq, num_pad_seq):
        try:
            value = map.get(Column.RETIREMENT_AGE)
            xpath = XPath.RETIREMENT_AGE_SELECT
            click(driver, xpath)
            time.sleep(1)
            click(driver, xpath)
            NumPad.click_number(driver, overlay_seq, num_pad_seq, value)
        except Exception as e:
            print(f"ERROR: Failed to set retirement age - {str(e)}")
            raise

    @staticmethod
    def set_anb(driver, map, overlay_seq):
        try:
            click(driver, XPath.ANB_SELECT)
            time.sleep(1)
            click(driver, XPath.ANB_SELECT)
            time.sleep(1)
            click(
                driver, XPath.ANB_YEAR_SELECT.format(seq=overlay_seq))
            click(driver, XPath.ANB_YEAR_VALUE)
            click(
                driver, XPath.ANB_MONTH_SELECT.format(seq=overlay_seq))
            click(driver, XPath.ANB_MONTH_VALUE)
            click(driver, XPath.ANB_DAY_VALUE)
            click(driver, XPath.ANB_CONFIRM.format(seq=overlay_seq))
        except Exception as e:
            print(f"ERROR: Failed to set ANB - {str(e)}")
            raise

    @staticmethod
    def set_extra_life(driver, map, overlay_seq, num_pad_seq):
        try:
            value = map.get(Column.EXTRA_LIFE)
            xpath = XPath.EXTRA_LIFE_SELECT
            click(driver, xpath)
            time.sleep(1)
            click(driver, xpath)
            NumPad.click_number(driver, overlay_seq, num_pad_seq, value)
        except Exception as e:
            print(f"ERROR: Failed to set extra life - {str(e)}")
            raise

    @staticmethod
    def set_extra_medical(driver, map, overlay_seq, num_pad_seq):
        try:
            value = map.get(Column.EXTRA_MEDICAL)
            xpath = XPath.EXTRA_MEDICAL_SELECT
            click(driver, xpath)
            NumPad.click_number(driver, overlay_seq, num_pad_seq, value)
        except Exception as e:
            print(f"ERROR: Failed to set extra medical - {str(e)}")
            raise

    @staticmethod
    def set_extra_saving(driver, map, overlay_seq, num_pad_seq):
        try:
            value = map.get(Column.EXTRA_SAVING)
            xpath = XPath.EXTRA_SAVING_SELECT
            click(driver, xpath)
            time.sleep(1)
            click(driver, xpath)
            NumPad.click_number(driver, overlay_seq, num_pad_seq, value)
        except Exception as e:
            print(f"ERROR: Failed to set extra saving - {str(e)}")
            raise

    @staticmethod
    def set_time_to_achieve(driver, map, overlay_seq, num_pad_seq):
        try:
            value = map.get(Column.TIME_TO_ACHIEVE)
            xpath = XPath.TIME_TO_ACHIEVE_SELECT
            click(driver, xpath)
            time.sleep(1)
            click(driver, xpath)
            NumPad.click_number(driver, overlay_seq, num_pad_seq, value)
        except Exception as e:
            print(f"ERROR: Failed to set time to achieve - {str(e)}")
            raise

    @staticmethod
    def set_objective(driver, map):
        try:
            value = map.get(Column.OBJECTIVE)
            print(f"INFO: Setting objective with value: {value}")

            # Split the value string and convert to element indices
            objectives = [x.strip().lower() for x in value.split(',')]
            indices = [OptionConstants.OBJECTIVE_OPTIONS[obj] for obj in objectives if obj in OptionConstants.OBJECTIVE_OPTIONS]

            print(f"INFO: Indices to click: {indices}")

            wait = WebDriverWait(driver, 10, 0.5)
            path = XPath.OBJECTIVE_SELECT

            element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, path)))
            print(f"INFO: Elements at {path} to be present")
            elements = driver.find_elements(By.CSS_SELECTOR, path)

            # Click each selected objective
            for index in indices:
                print(f"INFO: Clicking objective at index {index}")
                if index < len(elements):
                    try:
                        elements2 = driver.find_elements(By.CSS_SELECTOR, path)
                        element = elements2[index]
                        driver.execute_script("arguments[0].scrollIntoView(true);", element)
                        # Locate element again after scrolling
                        elements2 = driver.find_elements(By.CSS_SELECTOR, path)
                        element = elements2[index]
                        driver.execute_script("arguments[0].click();", element)
                        time.sleep(1)
                        # Locate element again
                        elements2 = driver.find_elements(By.CSS_SELECTOR, path)
                        element = elements2[index]
                        driver.execute_script("arguments[0].click();", element)
                    except StaleElementReferenceException:
                        print(f"ERROR: Stale element reference exception for index {index}")
                    time.sleep(1)
        except Exception as e:
            print(f"ERROR: Failed to set objective - {str(e)}")
            raise

    @staticmethod
    def set_target_period(driver, map):
        try:
            value = map.get(Column.TARGET_PERIOD)
            print(f"INFO: Setting Target Period with value: {value}")

            # Split the value string and convert to element indices
            target_period = [x.strip().lower() for x in value.split(',')]
            indices = [OptionConstants.TARGET_PERIOD_OPTIONS[obj] for obj in target_period if obj in OptionConstants.TARGET_PERIOD_OPTIONS]

            wait = WebDriverWait(driver, 10, 0.5)
            path = XPath.TARGET_PERIOD

            element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, path)))
            print(f"INFO: Elements at {path} to be present")
            elements = driver.find_elements(By.CSS_SELECTOR, path)

            # Click each selected objective
            for index in indices:
                print(f"INFO: Clicking objective at index {index}")
                if index < len(elements):
                    try:
                        elements2 = driver.find_elements(By.CSS_SELECTOR, path)
                        element = elements2[index]
                        driver.execute_script("arguments[0].scrollIntoView(true);", element)
                        # Locate element again after scrolling
                        elements2 = driver.find_elements(By.CSS_SELECTOR, path)
                        element = elements2[index]
                        driver.execute_script("arguments[0].click();", element)
                        time.sleep(1)
                        # Locate element again
                        elements2 = driver.find_elements(By.CSS_SELECTOR, path)
                        element = elements2[index]
                        driver.execute_script("arguments[0].click();", element)
                    except StaleElementReferenceException:
                        print(f"ERROR: Stale element reference exception for index {index}")
                    time.sleep(1)
            time.sleep(1)
        except Exception as e:
            print(f"ERROR: Failed to set objective - {str(e)}")
            raise

    @staticmethod
    def set_income_source(driver, map):
        try:
            wait = WebDriverWait(driver, 10, 0.5)
            path = "ion-radio-group"

            element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, path)))
            elements = driver.find_elements(By.CSS_SELECTOR, path)
            print(f"INFO: Elements at {path} to be present")
            element = elements[1]
            radio = element.find_elements(By.CSS_SELECTOR, "ion-radio")
            driver.execute_script("arguments[0].scrollIntoView(true);", radio[0])
            driver.execute_script("arguments[0].click();", radio[0])
            time.sleep(1)
            driver.execute_script("arguments[0].click();", radio[0])
            time.sleep(5)
        except Exception as e:
            print(f"ERROR: Failed to set income source - {str(e)}")
            raise

    @staticmethod
    def set_monthly_prem_expense(driver, map, overlay_seq, num_pad_seq):
        try:
            value = map.get(Column.MONTHLY_PREM_EXPENSE)
            xpath = XPath.MONTHLY_PREM_EXPENSE
            click(driver, xpath)
            time.sleep(1)
            click(driver, xpath)
            NumPad.click_number(driver, overlay_seq, num_pad_seq, value)
        except Exception as e:
            print(f"ERROR: Failed to set monthly premium expense - {str(e)}")
            raise

    @staticmethod
    def set_monthly_disposable_income(driver, map, overlay_seq, num_pad_seq):
        try:
            wait = WebDriverWait(driver, 10, 0.5)
            path = "ion-radio-group"

            element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, path)))
            elements = driver.find_elements(By.CSS_SELECTOR, path)
            print(f"INFO: Elements at {path} to be present")
            element = elements[2]
            radio = element.find_elements(By.CSS_SELECTOR, "ion-radio")
            driver.execute_script("arguments[0].scrollIntoView(true);", radio[0])
            driver.execute_script("arguments[0].click();", radio[0])

            value = map.get(Column.MONTHLY_DISPOSABLE_INCOME)
            xpath = XPath.MONTHLY_DISPOSABLE_INCOME
            click(driver, xpath)
            time.sleep(1)
            click(driver, xpath)
            NumPad.click_number(driver, overlay_seq, num_pad_seq, value)            

            time.sleep(5)
        except Exception as e:
            print(f"ERROR: Failed to set income source - {str(e)}")
            raise