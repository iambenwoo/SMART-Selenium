import os
import pandas as pd
from datetime import datetime

# Constants
DEFAULT_TEST_CASES_PATH = os.path.join(
    os.path.dirname(__file__), "../test_cases/test_cases.xlsx"
)
SHEET_ENV="ENV"
SHEET_CREDENTIALS="Credentials"
SHEET_CASES="Cases"
SHEET_TEST_SUITE="Test_Suite"

ENV_ENV_ID = "ENV_ID"
CASES_CASE_ID = "Case_ID"
CASE_LOGIN_ID = "Login_ID"


def read_sheet_as_array(sheet_name):
    """Reads the entire sheet as a DataFrame."""
    try:
        return pd.read_excel(DEFAULT_TEST_CASES_PATH, sheet_name=sheet_name)
    except Exception as e:
        raise ValueError(
            f"Failed to read sheet '{sheet_name}' as array: {str(e)}")


def read_cases_id_from_test_suite(suite_id):
    """Reads the Cases sheet and returns it as a DataFrame."""
    return read_sheet_as_array(suite_id)


def export_results_to_excel(results, suite_id):
    """Exports the test results to an Excel file."""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{suite_id}_{timestamp}.xlsx"
        pd.DataFrame(results).to_excel(output_file, index=False)
        print(f"Test results saved to {output_file}")
        return output_file
    except Exception as e:
        raise ValueError(f"Failed to export results to Excel: {str(e)}")


def read_case_data(env_id, case_id):
    """
    Reads a row from the 'Cases' sheet based on the case ID, appends data from the 'ENV' sheet,
    and includes data from the 'Credentials' sheet. Transforms the combined data into a dictionary,
    including only columns with non-blank headers.

    Args:
        case_id (str): The case ID to search for.
        env_id (str): The environment ID to search for.

    Returns:
        dict: A dictionary with column headers as keys and corresponding row values.
    """
    try:
        # Read data from the Cases sheet
        df_cases = pd.read_excel(DEFAULT_TEST_CASES_PATH, sheet_name=SHEET_CASES)
        row_cases = df_cases.loc[df_cases[CASES_CASE_ID] == case_id]
        if row_cases.empty:
            raise ValueError(f"No data found for Case ID: {case_id}")
        case_data = {col: row_cases[col].values[0] for col in df_cases.columns if col.strip()}

        # Read data from the ENV sheet
        df_env = pd.read_excel(DEFAULT_TEST_CASES_PATH, sheet_name=SHEET_ENV)
        row_env = df_env.loc[df_env[ENV_ENV_ID] == env_id]
        if not row_env.empty:
            env_data = {col: row_env[col].values[0] for col in df_env.columns if col.strip()}
            case_data.update(env_data)

        # Read data from the Credentials sheet
        login_id = case_data.get(CASE_LOGIN_ID)
        if login_id:
            df_credentials = pd.read_excel(DEFAULT_TEST_CASES_PATH, sheet_name=SHEET_CREDENTIALS)
            row_credentials = df_credentials.loc[df_credentials[CASE_LOGIN_ID] == login_id]
            if not row_credentials.empty:
                credentials_data = {col: row_credentials[col].values[0] for col in df_credentials.columns if col.strip()}
                case_data.update(credentials_data)

        return case_data
    except Exception as e:
        raise ValueError(f"Failed to read case data for Case ID '{case_id}' and ENV ID '{env_id}': {str(e)}")
