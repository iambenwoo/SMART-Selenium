import os
import pandas as pd
from datetime import datetime

# Constants
DEFAULT_TEST_CASES_PATH = os.path.join(
    os.path.dirname(__file__), "../test_cases/test_cases.xlsx"
)

def read_excel_value(sheet_name, row_key, key_column, value_column):
    """
    Reads a value from an Excel file based on a row key and specified columns.

    Args:
        sheet_name (str): Name of the sheet to read.
        row_key (str): The key to search for in the key column.
        key_column (str): The column name to match the row key.
        value_column (str): The column name to retrieve the value from.

    Returns:
        The value from the specified column for the matching row key.
    """
    try:
        print(f"Reading value from Excel: Sheet: {sheet_name}, Key: {row_key}, key_column: {key_column}, value_column: {value_column}")
        df = pd.read_excel(DEFAULT_TEST_CASES_PATH, sheet_name=sheet_name)
        return df.loc[df[key_column] == row_key, value_column].values[0]
    except Exception as e:
        raise ValueError(f"Failed to retrieve value for key '{row_key}' from Excel: {str(e)}")

def read_login_password(login_id):
    """
    Reads the password for a given login ID from the Credentials sheet.

    Args:
        login_id (str): The login ID.

    Returns:
        str: The password associated with the login ID.
    """
    return read_excel_value(
        sheet_name="Credentials",
        row_key=login_id,
        key_column="Login_ID",
        value_column="Password"
    )

def read_url(env_id):
    """
    Reads the URL for a given environment ID from the ENV sheet.

    Args:
        env_id (str): The environment ID.

    Returns:
        str: The URL associated with the environment ID.
    """
    print(f"Reading URL for environment ID: {env_id}")
    return read_excel_value(
        sheet_name="ENV",
        row_key=env_id,
        key_column="ENV_ID",
        value_column="URL"
    )

def read_case_login(case_id):
    """
    Reads the login ID for a given case ID from the Cases sheet.

    Args:
        case_id (str): The case ID.

    Returns:
        str: The login ID associated with the case ID.
    """
    return read_excel_value(
        sheet_name="Cases",
        row_key=case_id,
        key_column="Case_ID",
        value_column="Login_ID"
    )

def read_sheet_as_array(sheet_name):
    """
    Reads the entire sheet as a DataFrame.

    Args:
        sheet_name (str): Name of the sheet to read.

    Returns:
        DataFrame: A DataFrame representing the rows in the sheet.
    """
    try:
        print(f"Reading sheet: {sheet_name} as an array")
        return pd.read_excel(DEFAULT_TEST_CASES_PATH, sheet_name=sheet_name)
    except Exception as e:
        raise ValueError(f"Failed to read sheet '{sheet_name}' as array: {str(e)}")

def read_cases_id_from_test_suite(suite_id):
    """
    Reads the Cases sheet and returns it as a DataFrame.

    Args:
        suite_id (str): The suite ID to read.

    Returns:
        DataFrame: A DataFrame representing the rows in the Cases sheet.
    """
    return read_sheet_as_array(suite_id)

def export_results_to_excel(results, suite_id):
    """
    Exports the test results to an Excel file.

    Args:
        results (list): List of dictionaries containing test results.
        suite_id (str): Suite ID to include in the filename.

    Returns:
        str: The path to the exported Excel file.
    """
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{suite_id}_{timestamp}.xlsx"
        results_df = pd.DataFrame(results)
        results_df.to_excel(output_file, index=False)
        print(f"Test results saved to {output_file}")
        return output_file
    except Exception as e:
        raise ValueError(f"Failed to export results to Excel: {str(e)}")
