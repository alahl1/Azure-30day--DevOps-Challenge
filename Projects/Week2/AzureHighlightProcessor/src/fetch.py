# fetch.py

import json
import requests
from config import (
    API_URL,
    RAPIDAPI_HOST,
    RAPIDAPI_KEY,
    DATE,
    LEAGUE_NAME,
    LIMIT,
    AZURE_STORAGE_ACCOUNT_NAME,
    AZURE_STORAGE_ACCOUNT_KEY,
    AZURE_BLOB_CONTAINER_NAME,
)
from azure.storage.blob import BlobServiceClient

def fetch_highlights():
    try:
        query_params = {
            "date": DATE,
            "leagueName": LEAGUE_NAME,
            "limit": LIMIT
        }
        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": RAPIDAPI_HOST
        }
        response = requests.get(API_URL, headers=headers, params=query_params, timeout=120)
        response.raise_for_status()
        highlights = response.json()
        print("Highlights fetched successfully!")
        return highlights
    except requests.exceptions.RequestException as e:
        print(f"Error fetching highlights: {e}")
        return None

def save_to_blob(data, file_name):
    try:
        connection_str = (
            f"DefaultEndpointsProtocol=https;"
            f"AccountName={AZURE_STORAGE_ACCOUNT_NAME};"
            f"AccountKey={AZURE_STORAGE_ACCOUNT_KEY};"
            f"EndpointSuffix=core.windows.net"
        )
        blob_service_client = BlobServiceClient.from_connection_string(connection_str)
        
        # Force container name to lowercase to ensure it's valid.
        container_name = AZURE_BLOB_CONTAINER_NAME.lower()
        container_client = blob_service_client.get_container_client(container_name)
        if not container_client.exists():
            print(f"Container {container_name} does not exist. Creating...")
            container_client.create_container()
            print(f"Container {container_name} created successfully.")
        else:
            print(f"Container {container_name} exists.")
        
        blob_name = f"highlights/{file_name}.json"
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(json.dumps(data), overwrite=True)
        print(f"Highlights saved to Azure Blob Storage: {container_name}/{blob_name}")
    except Exception as e:
        print(f"Error saving to Blob Storage: {e}")

def process_highlights():
    print("Fetching highlights...")
    highlights = fetch_highlights()
    if highlights:
        print("Saving highlights to Azure Blob Storage...")
        save_to_blob(highlights, "basketball_highlights")

if __name__ == "__main__":
    process_highlights()
