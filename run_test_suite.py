import argparse
from automation.fna import FNA
from automation.data import (
    read_case_login,
    read_cases_id_from_test_suite,
    export_results_to_excel,
)  # Import necessary methods from data

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Run automation test.")
    parser.add_argument("--env_id", required=True, help="Environment to run the test (e.g., UAT7).")
    parser.add_argument("--suite_id", required=True, help="Suite ID to fetch test suites.")
    parser.add_argument("--export_results", action="store_true", help="Enable exporting results to an Excel file.")
    args = parser.parse_args()

    # Define parameters
    env_id = args.env_id
    suite_id = args.suite_id
    export_results = args.export_results

    # Prepare results list
    results = []

    try:
        # Read the sheet with the name suite_id
        df = read_cases_id_from_test_suite(suite_id)
        print(f"Running test suite: {suite_id} for environment: {env_id}")

        # Loop through each row in the Case_ID column
        for case_id in df["Case_ID"]:
            print(f"Processing Case ID: {case_id}")

            try:
                # Check if the Case_ID starts with "FNA"
                if case_id.startswith("FNA"):
                    # Retrieve the Login_ID for the current Case_ID
                    login_id = read_case_login(case_id)

                    # Create FNA instance and run the test
                    fna = FNA()
                    fna.perform_fna(env_id, login_id)
                    results.append({"Case_ID": case_id, "Result": "Success"})
                else:
                    print(f"Skipping Case ID: {case_id} as it does not start with 'FNA'.")
                    results.append({"Case_ID": case_id, "Result": "Skipped"})
            except Exception as case_error:
                print(f"Error processing Case ID '{case_id}': {case_error}")
                results.append({"Case_ID": case_id, "Result": f"Error: {case_error}"})

        # Export results to Excel if enabled
        if export_results:
            export_results_to_excel(results, suite_id)
        else:
            print("Exporting results to Excel is disabled.")

    except Exception as e:
        print(f"Error processing suite '{suite_id}': {e}")
        exit(1)
