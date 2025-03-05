#!/usr/bin/env python3
"""
update_env.py

This script retrieves Terraform outputs in JSON format and updates the .env file
with the new Azure Storage Account details:
  - AZURE_STORAGE_ACCOUNT_NAME
  - AZURE_STORAGE_ACCOUNT_KEY
  - AZURE_BLOB_CONTAINER_NAME

Usage:
    python update_env.py
"""

import json
import subprocess
import os

def get_terraform_outputs():
    """
    Executes 'terraform output -json' and returns the parsed JSON outputs.
    """
    try:
        # Run the terraform command to get outputs as JSON.
        result = subprocess.check_output(["terraform", "output", "-json"])
        outputs = json.loads(result.decode())
        return outputs
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving Terraform outputs: {e}")
        return None

def update_env_file(outputs):
    """
    Updates the .env file with the Terraform outputs.

    Args:
        outputs (dict): A dictionary of Terraform outputs.
    """
    env_file = ".env"
    # Load current .env lines
    with open(env_file, "r") as f:
        lines = f.readlines()

    # Extract needed values from Terraform outputs
    storage_account_name = outputs.get("storage_account_name", {}).get("value")
    storage_account_primary_key = outputs.get("storage_account_primary_key", {}).get("value")
    container_name = outputs.get("container_name", {}).get("value")

    if not (storage_account_name and storage_account_primary_key and container_name):
        print("Terraform outputs missing required values. Please check your Terraform configuration.")
        return

    # Prepare new .env contents by updating specific lines
    new_lines = []
    for line in lines:
        if line.startswith("AZURE_STORAGE_ACCOUNT_NAME="):
            new_lines.append(f"AZURE_STORAGE_ACCOUNT_NAME={storage_account_name}\n")
        elif line.startswith("AZURE_STORAGE_ACCOUNT_KEY="):
            new_lines.append(f"AZURE_STORAGE_ACCOUNT_KEY={storage_account_primary_key}\n")
        elif line.startswith("AZURE_BLOB_CONTAINER_NAME="):
            new_lines.append(f"AZURE_BLOB_CONTAINER_NAME={container_name}\n")
        else:
            new_lines.append(line)

    # Write the updated lines back to the .env file
    with open(env_file, "w") as f:
        f.writelines(new_lines)

    print(f".env updated with new Azure storage values:")
    print(f"  AZURE_STORAGE_ACCOUNT_NAME={storage_account_name}")
    print(f"  AZURE_BLOB_CONTAINER_NAME={container_name}")

if __name__ == "__main__":
    outputs = get_terraform_outputs()
    if outputs:
        update_env_file(outputs)
