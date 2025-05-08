import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from .utils import get_timestamp, open_url, initialize_driver, input_text


class XPath:
    # Locator constants
    LOGIN_ID_INPUT = "//input[@name='search']"
    PASSWORD_INPUT = "//div[@id='password']/div[2]/ion-input/input"

class Column:
    # Column constants
    LOGIN_ID = "Login_ID"
    PASSWORD = "Password"
    URL = "URL"

class Login:

    @staticmethod
    def perform_login(map):
        driver = initialize_driver()  # Get driver from utils

        try:
            login_id = map.get(Column.LOGIN_ID)
            password = map.get(Column.PASSWORD)

            # Open the URL using the driver
            open_url(driver, map.get(Column.URL))
            print(f"\nINFO: [{get_timestamp()}] Clicking login input\n")
            input_text(
                driver, XPath.LOGIN_ID_INPUT, login_id, Keys.ENTER)

            print(f"\nINFO: [{get_timestamp()}] Clicking password input\n")
            input_text(
                driver, XPath.PASSWORD_INPUT, password, Keys.ENTER)

        except Exception as e:
            print(
                f"\nERROR: [{get_timestamp()}] Failed during login operation - {str(e)}\n")
            raise

        return driver  # Return driver
