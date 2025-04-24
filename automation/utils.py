import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Constants
DEFAULT_WINDOW_SIZE = (1200, 926)
DEFAULT_TIMEOUT = 10
DEFAULT_POLL_FREQUENCY = 0.5
DEFAULT_TEST_CASES_PATH = os.path.join(os.path.dirname(__file__), "../test_cases/test_cases.xlsx")

@staticmethod
def initialize_driver(window_size=DEFAULT_WINDOW_SIZE):
    """Initializes and returns the WebDriver."""
    driver = webdriver.Chrome()
    driver.set_window_size(*window_size)
    return driver


def teardown_driver(driver):
    """Closes the WebDriver."""
    if driver:
        driver.quit()


def get_timestamp():
    """Returns the current timestamp in YYYY-MM-DD HH:MM:SS format."""
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def open_url(driver, url):
    """Navigates the WebDriver to the URL retrieved from the Excel file based on the given ID."""
    try:
        driver.get(url)
    except Exception as e:
        raise ValueError(f"Failed to open URL '{url}': {str(e)}")


def wait_for_disappear(driver, xpath, BY=By.XPATH):
    """Waits for an element to disappear from the DOM."""
    try:
        wait = WebDriverWait(driver, DEFAULT_TIMEOUT, DEFAULT_POLL_FREQUENCY)
        print(f"INFO: Waiting for element at {xpath} to disappear")
        wait.until(EC.invisibility_of_element_located((BY, xpath)))
    except Exception as e:
        print(f"ERROR: Failed to wait for element at {xpath} to disappear - {str(e)}")
        raise


def wait_and_click(driver, xpath):
    """Locates, scrolls to, and clicks an element."""
    try:
        wait = WebDriverWait(driver, DEFAULT_TIMEOUT, DEFAULT_POLL_FREQUENCY)
        element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        print(f"INFO: Clicking element at {xpath}")
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element.click()
    except Exception as e:
        print(f"ERROR: Failed to click element at {xpath} - {str(e)}")
        raise


def clear_and_enter_text(driver, xpath, text, additional_keys=None):
    """Clears and enters text into an element, optionally sending additional keys."""
    try:
        wait = WebDriverWait(driver, DEFAULT_TIMEOUT, DEFAULT_POLL_FREQUENCY)
        element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        print(f"INFO: Clearing and entering text at {xpath}")
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element.click()
        element.clear()
        element.send_keys(text)
        if additional_keys:
            element.send_keys(additional_keys)
    except Exception as e:
        print(f"ERROR: Failed to clear and enter text at {xpath} - {str(e)}")
        raise


class NumPad:
    @staticmethod
    def get_digit_xpath(overlay_id, digit):
        """
        Generates the XPath for a calculator digit button based on the overlay ID and digit.

        Args:
            overlay_id (str): The ID of the overlay.
            digit (int): The digit to generate the XPath for (0-9).

        Returns:
            str: The XPath for the specified digit button.
        """
        digit_map = {
            0: "//ion-modal[@id='{overlay_id}']/div/nano-number-pad/div/div[3]/div[3]/ion-button[4]",
            1: "//ion-modal[@id='{overlay_id}']/div/nano-number-pad/div/div[3]/div[3]/ion-button[3]",
            2: "//ion-modal[@id='{overlay_id}']/div/nano-number-pad/div/div[3]/div[2]/ion-button[3]",
            3: "//ion-modal[@id='{overlay_id}']/div/nano-number-pad/div/div[3]/div[3]/ion-button[3]",
            4: "//ion-modal[@id='{overlay_id}']/div/nano-number-pad/div/div[3]/div[1]/ion-button[2]",
            5: "//ion-modal[@id='{overlay_id}']/div/nano-number-pad/div/div[3]/div[2]/ion-button[2]",
            6: "//ion-modal[@id='{overlay_id}']/div/nano-number-pad/div/div[3]/div[3]/ion-button[2]",
            7: "//ion-modal[@id='{overlay_id}']/div/nano-number-pad/div/div[3]/div[1]/ion-button",
            8: "//ion-modal[@id='{overlay_id}']/div/nano-number-pad/div/div[3]/div[2]/ion-button",
            9: "//ion-modal[@id='{overlay_id}']/div/nano-number-pad/div/div[3]/div[3]/ion-button",
        }

        if digit not in digit_map:
            raise ValueError(f"Invalid digit: {digit}")

        return digit_map[digit].format(overlay_id=overlay_id)

    @staticmethod
    def wait_and_click(driver, overlay_id, number):
        """
        Splits the number into digits and waits for and clicks each digit button.

        Args:
            driver: WebDriver instance.
            overlay_id (str): The ID of the overlay.
            number (int): The number to click, split into digits.
        """
        NUMPAD_CLEAR = "//ion-modal[@id='{overlay_id}']/div/nano-number-pad/div/div[3]/div/ion-button[5]"
        NUMPAD_CONFIRM = "//ion-modal[@id='{overlay_id}']/div/nano-number-pad/div/div[3]/div[3]/ion-button[5]"
    
        wait_and_click(driver, NUMPAD_CLEAR.format(overlay_id=overlay_id))

        for digit in str(number):
            xpath = NumPad.get_digit_xpath(overlay_id, int(digit))
            wait_and_click(driver, xpath)

        wait_and_click(driver, NUMPAD_CONFIRM.format(overlay_id=overlay_id))
