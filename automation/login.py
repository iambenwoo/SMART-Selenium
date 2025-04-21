import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from . import utils  # Import the entire utils module
from .utils import get_timestamp, open_url, initialize_driver  # Updated import
from .data import read_login_password  # Import read_excel_value from data.py


class Login:
    # Locator constants
    LOGIN_ID_PATH = "//input[@name='search']"
    PASSWORD_PATH = "//div[@id='password']/div[2]/ion-input/input"

    @staticmethod
    def perform_login(env_id, login_id):
        driver = initialize_driver()  # Get driver from utils

        try:
            password = read_login_password(
                login_id,
            )
            # Use the env_id parameter to open the URL
            open_url(driver, env_id)
            print(f"\nINFO: [{get_timestamp()}] Clicking login input\n")
            utils.clear_and_enter_text(
                driver, Login.LOGIN_ID_PATH, login_id, Keys.ENTER)

            print(f"\nINFO: [{get_timestamp()}] Clicking password input\n")
            utils.clear_and_enter_text(
                driver, Login.PASSWORD_PATH, password, Keys.ENTER)

        except Exception as e:
            print(
                f"\nERROR: [{get_timestamp()}] Failed during login operation - {str(e)}\n")
            raise

        return driver  # Return driver
