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
    AZURE_STORAGE_CONNECTION_STRING,
    AZURE_BLOB_CONTAINER_NAME,
)
from azure.storage.blob import BlobServiceClient

def fetch_highlights():
    try:
        # Prepare query parameters for the API request.
        query_params = {
            "date": DATE,
            "leagueName": LEAGUE_NAME,
            "limit": LIMIT
        }
        # Set headers required for RapidAPI authentication.
        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": RAPIDAPI_HOST
        }
        # Make the GET request to the API.
        response = requests.get(API_URL, headers=headers, params=query_params, timeout=120)
        response.raise_for_status()  # Raise an error for non-200 responses.
        highlights = response.json()  # Parse the response JSON.
        print("Highlights fetched successfully!")
        return highlights
    except requests.exceptions.RequestException as e:
        print(f"Error fetching highlights: {e}")
        return None

def save_to_blob(data, file_name):
    try:
        # Create the BlobServiceClient using the connection string from config.
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
        
        # Ensure the container name is in lowercase.
        container_name = AZURE_BLOB_CONTAINER_NAME.lower()
        container_client = blob_service_client.get_container_client(container_name)
        if not container_client.exists():
            print(f"Container {container_name} does not exist. Creating...")
            container_client.create_container()
            print(f"Container {container_name} created successfully.")
        else:
            print(f"Container {container_name} exists.")
        
        # Construct the blob name/path.
        blob_name = f"highlights/{file_name}.json"
        blob_client = container_client.get_blob_client(blob_name)
        # Upload the JSON data (as a string) to Blob Storage.
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
