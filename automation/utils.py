import time
import pandas as pd  # Added for reading Excel files
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from .data import read_url  # Importing from data.py

# Constants
DEFAULT_WINDOW_SIZE = (1200, 926)
DEFAULT_TIMEOUT = 10
DEFAULT_POLL_FREQUENCY = 0.5
DEFAULT_TEST_CASES_PATH = os.path.join(os.path.dirname(__file__), "../test_cases/test_cases.xlsx")

def initialize_driver(window_size=DEFAULT_WINDOW_SIZE):
    """
    Initializes and returns the WebDriver and WebDriverWait instances.
    """
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

def open_url(driver, env_id):
    """
    Navigates the WebDriver to the URL retrieved from the Excel file based on the given ID.
    """
    try:
        # Use the reusable function to get the URL
        print(f"Opening URL for ID: {env_id}")
        url = read_url(env_id)
        driver.get(url)
    except Exception as e:
        raise ValueError(f"Failed to open URL for ID '{env_id}': {str(e)}")

def wait_for_disappear(driver, xpath, BY=By.XPATH):

    """
    Waits for an element to disappear from the DOM.

    Args:
        driver: WebDriver instance.
        xpath: XPath of the element to wait for.
    """
    try:
        wait = WebDriverWait(driver, DEFAULT_TIMEOUT, DEFAULT_POLL_FREQUENCY)
        print(f"\nINFO: Waiting for element at {xpath} to disappear\n")
        wait.until(EC.invisibility_of_element_located((BY, xpath)))
    except Exception as e:
        print(f"\nERROR: Failed to wait for element at {xpath} to disappear - {str(e)}\n")
        raise

def wait_and_click(driver, xpath):
    """
    Utility method to locate, scroll to, and click an element.
    """
    try:
        wait = WebDriverWait(driver, DEFAULT_TIMEOUT, DEFAULT_POLL_FREQUENCY)
        element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        if driver:
            print(f"\nINFO: Scrolling to element at {xpath}\n")
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
        print(f"\nINFO: Waiting for element at {xpath} to be clickable\n")
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        print(f"\nINFO: Clicking element at {xpath}\n")
        element.click()
    except Exception as e:
        print(f"\nERROR: Failed to click element at {xpath} - {str(e)}\n")
        raise

def clear_and_enter_text(driver, xpath, text, additional_keys=None):
    """
    Utility method to locate, scroll to, wait for clickable, clear, and enter text into an element.
    Optionally sends additional keys (e.g., Keys.ENTER).

    Args:
        driver: WebDriver instance.
        wait: WebDriverWait instance.
        xpath: XPath of the element.
        text: Text to enter into the element.
        additional_keys: Optional additional keys to send (e.g., Keys.ENTER).
    """
    try:
        wait = WebDriverWait(driver, DEFAULT_TIMEOUT, DEFAULT_POLL_FREQUENCY)
        element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        if driver:
            print(f"\nINFO: Scrolling to element at {xpath}\n")
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
        print(f"\nINFO: Waiting for element at {xpath} to be clickable\n")
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        print(f"\nINFO: Clearing and entering text at {xpath}\n")
        element.click()
        element.clear()
        element.send_keys(text)
        if additional_keys:
            print(f"\nINFO: Sending additional keys at {xpath}\n")
            element.send_keys(additional_keys)
    except Exception as e:
        print(f"\nERROR: Failed to clear and enter text at {xpath} - {str(e)}\n")
        raise
