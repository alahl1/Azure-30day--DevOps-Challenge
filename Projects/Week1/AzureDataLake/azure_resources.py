from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.synapse import SynapseManagementClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()

def create_storage_account(resource_group, storage_account_name, location, subscription_id):
    """Create Azure Storage Account and return connection string."""
    storage_client = StorageManagementClient(credential, subscription_id)
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
    keys = storage_client.storage_accounts.list_keys(resource_group, storage_account_name)
    connection_string = f"DefaultEndpointsProtocol=https;AccountName={storage_account_name};AccountKey={keys.keys[0].value};EndpointSuffix=core.windows.net"
    return connection_string

def create_synapse_workspace(resource_group, workspace_name, location, storage_account_name, subscription_id):
    """Create Synapse Analytics Workspace and return SQL endpoint."""
    synapse_client = SynapseManagementClient(credential, subscription_id)
    synapse_async_operation = synapse_client.workspaces.begin_create_or_update(
        resource_group,
        workspace_name,
        {
            "location": location,
            "default_data_lake_storage": {
                "account_url": f"https://{storage_account_name}.dfs.core.windows.net",
                "filesystem": "synapse",
            },
            "sql_administrator_login": "admin_user",
            "sql_administrator_login_password": "your_secure_password",
        },
    )
    workspace = synapse_async_operation.result()
    sql_endpoint = workspace.connectivity_endpoints["sql"]
    return sql_endpoint
