import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from .utils import get_timestamp, open_url, initialize_driver, clear_and_enter_text


class XPath:
    # Locator constants
    LOGIN_ID_PATH = "//input[@name='search']"
    PASSWORD_PATH = "//div[@id='password']/div[2]/ion-input/input"


class Login:

    @staticmethod
    def perform_login(map):
        driver = initialize_driver()  # Get driver from utils

        try:
            login_id = map.get("Login_ID")
            password = map.get("Password")

            # Open the URL using the driver
            open_url(driver, map.get("URL"))
            print(f"\nINFO: [{get_timestamp()}] Clicking login input\n")
            clear_and_enter_text(
                driver, XPath.LOGIN_ID_PATH, login_id, Keys.ENTER)

            print(f"\nINFO: [{get_timestamp()}] Clicking password input\n")
            clear_and_enter_text(
                driver, XPath.PASSWORD_PATH, password, Keys.ENTER)

        except Exception as e:
            print(
                f"\nERROR: [{get_timestamp()}] Failed during login operation - {str(e)}\n")
            raise

        return driver  # Return driver
