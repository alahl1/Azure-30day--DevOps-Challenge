# create_storage_account.py

import os
import string
import random
from azure.identity import DefaultAzureCredential
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.resource import ResourceManagementClient

def generate_storage_account_name(prefix="stor", length=12):
    # Generate a storage account name that conforms to Azure naming rules:
    # between 3 and 24 characters, lowercase letters and numbers only.
    random_part = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length - len(prefix)))
    return prefix + random_part

def update_env_file(account_name, account_key):
    env_file = ".env"
    new_lines = []
    with open(env_file, "r") as f:
        lines = f.readlines()
    found_name = False
    found_key = False
    for line in lines:
        if line.startswith("AZURE_STORAGE_ACCOUNT_NAME="):
            new_lines.append(f"AZURE_STORAGE_ACCOUNT_NAME={account_name}\n")
            found_name = True
        elif line.startswith("AZURE_STORAGE_ACCOUNT_KEY="):
            new_lines.append(f"AZURE_STORAGE_ACCOUNT_KEY={account_key}\n")
            found_key = True
        else:
            new_lines.append(line)
    if not found_name:
        new_lines.append(f"AZURE_STORAGE_ACCOUNT_NAME={account_name}\n")
    if not found_key:
        new_lines.append(f"AZURE_STORAGE_ACCOUNT_KEY={account_key}\n")
    with open(env_file, "w") as f:
        f.writelines(new_lines)
    print(f".env updated with storage account: {account_name}")

def create_storage_account():
    subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
    resource_group = os.getenv("AZURE_RESOURCE_GROUP")
    location = os.getenv("AZURE_LOCATION", "eastus")
    
    if not subscription_id or not resource_group:
        print("AZURE_SUBSCRIPTION_ID and AZURE_RESOURCE_GROUP must be set in the .env file.")
        return

    credential = DefaultAzureCredential()
    
    # Ensure the resource group exists. If not, create it.
    resource_client = ResourceManagementClient(credential, subscription_id)
    print(f"Ensuring resource group '{resource_group}' exists...")
    resource_client.resource_groups.create_or_update(
        resource_group,
        {"location": location}
    )
    print(f"Resource group '{resource_group}' is ready.")
    
    # Create the storage account.
    storage_client = StorageManagementClient(credential, subscription_id)
    storage_account_name = generate_storage_account_name()
    print(f"Creating storage account: {storage_account_name} in resource group: {resource_group} at location: {location}...")
    
    async_create = storage_client.storage_accounts.begin_create(
        resource_group_name=resource_group,
        account_name=storage_account_name,
        parameters={
            "location": location,
            "sku": {"name": "Standard_LRS"},
            "kind": "StorageV2",
        }
    )
    async_create.result()  # Wait for the creation to finish
    print(f"Storage account {storage_account_name} created.")
    
    # Retrieve the primary key for the new storage account.
    keys_result = storage_client.storage_accounts.list_keys(resource_group, storage_account_name)
    keys = keys_result.keys
    primary_key = None
    for key in keys:
        if key.key_name == "key1":
            primary_key = key.value
            break
    if not primary_key:
        print("Could not retrieve primary key for the storage account.")
        return
    
    update_env_file(storage_account_name, primary_key)

if __name__ == "__main__":
    create_storage_account()
