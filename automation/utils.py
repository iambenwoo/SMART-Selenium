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
DEFAULT_TEST_CASES_PATH = os.path.join(
    os.path.dirname(__file__), "../test_cases/test_cases.xlsx")


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
        print(
            f"ERROR: Failed to wait for element at {xpath} to disappear - {str(e)}")
        raise


def click(driver, xpath):
    """Locates, scrolls to, and clicks an element."""
    try:
        wait = WebDriverWait(driver, DEFAULT_TIMEOUT, DEFAULT_POLL_FREQUENCY)
        print(f"INFO: Waiting for element at {xpath} to be present")
        element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        print(f"INFO: Scrolling to element at {xpath} successfully")
        print(f"INFO: Element enabled status: {element.is_enabled(), element.is_displayed(), element.is_selected()}")
        print(f"INFO: Waiting for element at {xpath}")
        wait.until(EC.element_to_be_clickable((element)))
        try:
            print(f"INFO: Clicking element at {xpath}")
            #time.sleep(2)
            #driver.find_element(By.XPATH, xpath).click()
            element.click()

        except Exception:   
            time.sleep(1)
            element.click()
            raise
    except Exception as e:
        print(f"ERROR: Failed to click element at {xpath} - {str(e)}")
        raise

def click_by_CSS(driver, css_path):
    """Locates, scrolls to, and clicks an element using CSS selector."""
    try:
        wait = WebDriverWait(driver, DEFAULT_TIMEOUT, DEFAULT_POLL_FREQUENCY)
        print(f"INFO: Waiting for element at {css_path} to be present")
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_path)))
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        print(f"INFO: Scrolling to element at {css_path} successfully")
        print(f"INFO: Element enabled status: {element.is_enabled(), element.is_displayed(), element.is_selected()}")
        print(f"INFO: Waiting for element at {css_path}")
        wait.until(EC.element_to_be_clickable((element)))
        try:
            print(f"INFO: Clicking element at {css_path}")
            #time.sleep(2)
            element.click()

        except Exception:   
            time.sleep(1)
            element.click()
            raise
    except Exception as e:
        print(f"ERROR: Failed to click element at {css_path} - {str(e)}")
        raise

def input_text(driver, xpath, text, additional_keys=None):
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

    CLEAR_BUTTON = "//ion-modal[@id='ion-overlay-{seq}']/div/nano-number-pad/div/div[{num_pad_seq}]/div/ion-button[5]"
    CONFIRM_BUTTON = "//ion-modal[@id='ion-overlay-{seq}']/div/nano-number-pad/div/div[{num_pad_seq}]/div[3]/ion-button[5]"

    DIGIT_MAP = {
        0: "//ion-modal[@id='ion-overlay-{seq}']/div/nano-number-pad/div/div[{num_pad_seq}]/div/ion-button[4]",
        1: "//ion-modal[@id='ion-overlay-{seq}']/div/nano-number-pad/div/div[{num_pad_seq}]/div/ion-button[3]",
        2: "//ion-modal[@id='ion-overlay-{seq}']/div/nano-number-pad/div/div[{num_pad_seq}]/div[2]/ion-button[3]",
        3: "//ion-modal[@id='ion-overlay-{seq}']/div/nano-number-pad/div/div[{num_pad_seq}]/div[3]/ion-button[3]",
        4: "//ion-modal[@id='ion-overlay-{seq}']/div/nano-number-pad/div/div[{num_pad_seq}]/div/ion-button[2]",
        5: "//ion-modal[@id='ion-overlay-{seq}']/div/nano-number-pad/div/div[{num_pad_seq}]/div[2]/ion-button[2]",
        6: "//ion-modal[@id='ion-overlay-{seq}']/div/nano-number-pad/div/div[{num_pad_seq}]/div[3]/ion-button[2]",
        7: "//ion-modal[@id='ion-overlay-{seq}']/div/nano-number-pad/div/div[{num_pad_seq}]/div/ion-button",
        8: "//ion-modal[@id='ion-overlay-{seq}']/div/nano-number-pad/div/div[{num_pad_seq}]/div[2]/ion-button",
        9: "//ion-modal[@id='ion-overlay-{seq}']/div/nano-number-pad/div/div[{num_pad_seq}]/div[3]/ion-button",
    }

    @staticmethod
    def click_number(driver, overlay_seq, num_pad_seq, number):
        """
        Splits the number into digits and waits for and clicks each digit button.

        Args:
            driver: WebDriver instance.
            overlay_id (str): The ID of the overlay.
            number (int): The number to click, split into digits.
        """

        click(driver, NumPad.CLEAR_BUTTON.format(
            seq=overlay_seq, num_pad_seq=num_pad_seq))

        print(f"INFO: Clicking number {number} on numpad")
        for digit in str(number):
            xpath = NumPad.DIGIT_MAP[int(digit)].format(
                seq=overlay_seq, num_pad_seq=num_pad_seq)
            click(driver, xpath)

        click(driver, NumPad.CONFIRM_BUTTON.format(
            seq=overlay_seq, num_pad_seq=num_pad_seq))
        time.sleep(1)
