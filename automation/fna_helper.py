from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .utils import get_timestamp, clear_and_enter_text, wait_and_click, wait_for_disappear
import time

class FNAHelpers:

    # Locator constants
    ION_BACKDROP_SELECTOR = "ion-backdrop.sc-ion-loading-ios.ios.backdrop-no-tappable.hydrated"

    # Button locators
    FNA_START_NEW_BUTTON = "(.//*[normalize-space(text()) and normalize-space(.)='財務需要分析'])[2]/following::button[1]"

    # Locator constants for name inputs
    FAMILY_NAME_INPUT = "//div[@id='familyName']/div[2]/ion-input/input"
    GIVEN_NAME_INPUT = "//div[@id='givenName']/div[2]/ion-input/input"
    
    # Locator constants for mobile number input
    MOBILE_NUMBER_INPUT = "//div[@id='mobile']/div[2]/ion-input/input"
    
    CALENDER_INPUT = "xpath=//div[@id='applicant']/div[2]/nano-field[3]/span/nano-date/div/div[2]/div/ion-icon"
    
    # Locator constants for marital status and number of dependents
    NUMBER_OF_DEPENDENT_INPUT = "(.//*[normalize-space(text()) and normalize-space(.)='受養人數目'])[1]/following::ion-select[1]"
    NUMBER_OF_DEPDENT_NIL="//ion-popover[@id='ion-overlay-4']/div/div[2]/ion-select-popover/ion-list/ion-radio-group/ion-item/ion-radio"
    NUMBER_OF_DEPDENT_1_3="//ion-popover[@id='ion-overlay-4']/div/div[2]/ion-select-popover/ion-list/ion-radio-group/ion-item[2]/ion-radio"
    NUMBER_OF_DEPDENT_4_6="//ion-popover[@id='ion-overlay-4']/div/div[2]/ion-select-popover/ion-list/ion-radio-group/ion-item[3]/ion-radio"
    NUMBER_OF_DEPDENT_7_ABOVE="//ion-popover[@id='ion-overlay-4']/div/div[2]/ion-select-popover/ion-list/ion-radio-group/ion-item[4]/ion-radio"

    # Locator constants for marital status options
    MARITAL_STATUS_SELECT = "(.//*[normalize-space(text()) and normalize-space(.)='婚姻狀況'])[1]/following::ion-select[1]"
    MARITAL_STATUS_SINGLE = "//ion-popover[@id='ion-overlay-3']/div/div[2]/ion-select-popover/ion-list/ion-radio-group/ion-item/ion-radio"
    MARITAL_STATUS_MARRIED = "//ion-popover[@id='ion-overlay-3']/div/div[2]/ion-select-popover/ion-list/ion-radio-group/ion-item[2]/ion-radio"
    MARITAL_STATUS_DIVORCED = "//ion-popover[@id='ion-overlay-3']/div/div[2]/ion-select-popover/ion-list/ion-radio-group/ion-item[3]/ion-radio"
    MARITAL_STATUS_WIDOWED = "//ion-popover[@id='ion-overlay-3']/div/div[2]/ion-select-popover/ion-list/ion-radio-group/ion-item[4]/ion-radio"

    @staticmethod
    def input_english_name(driver, family_name, given_name):
        """
        Helper method to input family name and given name using utility functions.
        """
        try:
            print(f"\nINFO: [{get_timestamp()}] Inputting family name\n")
            clear_and_enter_text(driver, FNAHelpers.FAMILY_NAME_INPUT, family_name)

            print(f"\nINFO: [{get_timestamp()}] Inputting given name\n")
            clear_and_enter_text(driver, FNAHelpers.GIVEN_NAME_INPUT, given_name)
        except Exception as e:
            print(f"\nERROR: Failed to input names - {str(e)}\n")
            raise
        
    @staticmethod
    def input_mobile_number(driver, mobile_number):
        """
        Helper method to input mobile number.
        """
        try:
            print(f"\nINFO: [{get_timestamp()}] Inputting mobile number\n")
            clear_and_enter_text(driver, FNAHelpers.MOBILE_NUMBER_INPUT, mobile_number)
        except Exception as e:
            print(f"\nERROR: Failed to input mobile number - {str(e)}\n")
            raise

    @staticmethod
    def set_marital_status(driver, marital_status):
        """
        Helper method to set marital status.
        """
        try:
            print(f"\nINFO: [{get_timestamp()}] Clicking marital status select\n")
            wait_and_click(driver, FNAHelpers.MARITAL_STATUS_SELECT)
            time.sleep(1)
            wait_and_click(driver, FNAHelpers.MARITAL_STATUS_SELECT)

            match marital_status:
                case "single":
                    MARITAL_STATUS_OPTION = FNAHelpers.MARITAL_STATUS_SINGLE
                case "married":
                    MARITAL_STATUS_OPTION = FNAHelpers.MARITAL_STATUS_MARRIED
                case "divorced":
                    MARITAL_STATUS_OPTION = FNAHelpers.MARITAL_STATUS_DIVORCED
                case "widowed":
                    MARITAL_STATUS_OPTION = FNAHelpers.MARITAL_STATUS_WIDOWED
                case _:
                    raise ValueError(f"Invalid marital status: {marital_status}")

            wait_and_click(driver, MARITAL_STATUS_OPTION)
            time.sleep(1)
        except Exception as e:
            print(f"\nERROR: Failed to set marital status - {str(e)}\n")
            raise

    @staticmethod
    def set_number_of_dependents(driver, number_of_dependents):
        """
        Helper method to set the number of dependents.
        """
        try:
            print(f"\nINFO: [{get_timestamp()}] Clicking number of dependents select\n")
            wait_and_click(driver, FNAHelpers.NUMBER_OF_DEPENDENT_INPUT)

            match number_of_dependents:
                case "nil":
                    NUMBER_OF_DEPENDENTS_OPTION = FNAHelpers.NUMBER_OF_DEPDENT_NIL
                case "1-3":
                    NUMBER_OF_DEPENDENTS_OPTION = FNAHelpers.NUMBER_OF_DEPDENT_1_3
                case "4-6":
                    NUMBER_OF_DEPENDENTS_OPTION = FNAHelpers.NUMBER_OF_DEPDENT_4_6
                case "7-above":
                    NUMBER_OF_DEPENDENTS_OPTION = FNAHelpers.NUMBER_OF_DEPDENT_7_ABOVE
                case _:
                    raise ValueError(f"Invalid number of dependents: {number_of_dependents}")

            wait_and_click(driver, NUMBER_OF_DEPENDENTS_OPTION)
            time.sleep(1)
        except Exception as e:
            print(f"\nERROR: Failed to set number of dependents - {str(e)}\n")
            raise

    @staticmethod
    def start_new_fna(driver):
        """
        Waits for the loading spinner to disappear and clicks the specified button.

        Args:
            wait: WebDriverWait instance.
        """
        try:
            print(f"\nINFO: [{get_timestamp()}] Waiting for loading spinner to disappear\n")
            wait_for_disappear(driver, FNAHelpers.ION_BACKDROP_SELECTOR, By.CSS_SELECTOR)
            time.sleep(10)
            print(f"\nINFO: [{get_timestamp()}] Clicking button at {FNAHelpers.FNA_START_NEW_BUTTON}\n")
            wait_and_click(driver, FNAHelpers.FNA_START_NEW_BUTTON)
        except Exception as e:
            print(f"\nERROR: Failed to wait for spinner and click button - {str(e)}\n")
            raise
