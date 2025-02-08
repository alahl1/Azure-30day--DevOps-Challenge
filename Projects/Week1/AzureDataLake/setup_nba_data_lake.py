from azure_resources import create_storage_account, create_synapse_workspace
from data_operations import fetch_nba_data, upload_to_blob_storage
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def main():
    # Azure configurations
    resource_group = os.getenv("AZURE_RESOURCE_GROUP")
    location = os.getenv("AZURE_LOCATION")
    storage_account_name = os.getenv("AZURE_STORAGE_ACCOUNT")
    subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
    workspace_name = os.getenv("SYNAPSE_WORKSPACE_NAME")

    # Step 1: Create Azure resources
    print("Creating Azure resources...")
    connection_string = create_storage_account(resource_group, storage_account_name, location, subscription_id)
    sql_endpoint = create_synapse_workspace(resource_group, workspace_name, location, storage_account_name, subscription_id)

    # Step 2: Save connection details to .env
    with open(".env", "a") as env_file:
        env_file.write(f"AZURE_CONNECTION_STRING={connection_string}\n")
        env_file.write(f"SYNAPSE_SQL_ENDPOINT={sql_endpoint}\n")
    print(".env file updated with Azure resource details.")

    # Step 3: Fetch and upload NBA data
    print("Fetching NBA data and uploading to Azure Blob Storage...")
    nba_data = fetch_nba_data()
    if nba_data:
        upload_to_blob_storage(nba_data, connection_string)

    print("Data lake setup complete.")

if __name__ == "__main__":
    main()
