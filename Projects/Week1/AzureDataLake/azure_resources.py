from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.synapse import SynapseManagementClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve credentials from environment variables
SQL_ADMIN_LOGIN = os.getenv("SQL_ADMIN_LOGIN")
SQL_ADMIN_PASSWORD = os.getenv("SQL_ADMIN_PASSWORD")
if not SQL_ADMIN_LOGIN or not SQL_ADMIN_PASSWORD:
    raise ValueError("❌ ERROR: SQL_ADMIN_LOGIN and SQL_ADMIN_PASSWORD must be set in the .env file.")

# Initialize Azure authentication
credential = DefaultAzureCredential()

def create_resource_group(resource_group_name, location, subscription_id):
    """Ensure the Azure Resource Group exists before creating resources."""
    resource_client = ResourceManagementClient(credential, subscription_id)
    try:
        resource_client.resource_groups.create_or_update(
            resource_group_name, {"location": location}
        )
        print(f"✅ Resource group '{resource_group_name}' created or already exists.")
    except Exception as e:
        print(f"❌ Error creating resource group: {e}")
        raise


def create_storage_account(resource_group, storage_account_name, location, subscription_id):
    """Create Azure Storage Account and return the connection string."""
    storage_client = StorageManagementClient(credential, subscription_id)

    # Ensure the resource group exists before proceeding
    create_resource_group(resource_group, location, subscription_id)

    try:
        print(f"⏳ Creating storage account '{storage_account_name}'...")
        storage_async_operation = storage_client.storage_accounts.begin_create(
            resource_group,
            storage_account_name,
            {
                "location": location,
                "sku": {"name": "Standard_LRS"},
                "kind": "StorageV2",
            },
        )
        storage_account = storage_async_operation.result()
        print(f"✅ Storage account '{storage_account_name}' created successfully.")

        # Get the connection string
        keys = storage_client.storage_accounts.list_keys(resource_group, storage_account_name)
        connection_string = f"DefaultEndpointsProtocol=https;AccountName={storage_account_name};AccountKey={keys.keys[0].value};EndpointSuffix=core.windows.net"
        return connection_string

    except Exception as e:
        print(f"❌ Error creating storage account '{storage_account_name}': {e}")
        raise


def create_synapse_workspace(resource_group, workspace_name, location, storage_account_name, subscription_id):
    """Create an Azure Synapse Analytics Workspace and return the SQL endpoint."""
    synapse_client = SynapseManagementClient(credential, subscription_id)

    # Ensure the resource group exists before proceeding
    create_resource_group(resource_group, location, subscription_id)

    try:
        print(f"⏳ Creating Synapse workspace '{workspace_name}'...")

        # Correcting the function call to include the required 'workspace_info' argument
        workspace_info = {
            "location": location,
            "identity": {"type": "SystemAssigned"},  # Enable System Assigned Identity
            "default_data_lake_storage": {
                "account_url": f"https://{storage_account_name}.dfs.core.windows.net",
                "filesystem": "synapse",
            },
            "sql_administrator_login": SQL_ADMIN_LOGIN,
            "sql_administrator_login_password": SQL_ADMIN_PASSWORD,
        }

        synapse_async_operation = synapse_client.workspaces.begin_create_or_update(
            resource_group_name=resource_group,
            workspace_name=workspace_name,
            workspace_info=workspace_info,  # Ensure this argument is passed
        )

        workspace = synapse_async_operation.result()
        sql_endpoint = workspace.connectivity_endpoints["sql"]
        print(f"✅ Synapse workspace '{workspace_name}' created successfully. SQL Endpoint: {sql_endpoint}")
        return sql_endpoint

    except Exception as e:
        print(f"❌ Error creating Synapse workspace '{workspace_name}': {e}")
        raise

        workspace = synapse_async_operation.result()
        sql_endpoint = workspace.connectivity_endpoints["sql"]
        print(f"✅ Synapse workspace '{workspace_name}' created successfully. SQL Endpoint: {sql_endpoint}")
        return sql_endpoint

    except Exception as e:
        print(f"❌ Error creating Synapse workspace '{workspace_name}': {e}")
        raise
