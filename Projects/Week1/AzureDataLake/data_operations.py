from azure.storage.blob import BlobServiceClient
import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()

def fetch_nba_data():
    """Fetch NBA player data from sportsdata.io."""
    api_key = os.getenv("SPORTS_DATA_API_KEY")
    nba_endpoint = os.getenv("NBA_ENDPOINT")
    try:
        headers = {"Ocp-Apim-Subscription-Key": api_key}
        response = requests.get(nba_endpoint, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching NBA data: {e}")
        return []

def upload_to_blob_storage(data, connection_string):
    """Upload NBA data to Azure Blob Storage."""
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_name = "nba-datalake"
    blob_name = "raw-data/nba_player_data.jsonl"

    # Convert data to line-delimited JSON
    line_delimited_data = "\n".join([json.dumps(record) for record in data])

    # Upload to Blob Storage
    container_client = blob_service_client.get_container_client(container_name)
    container_client.create_container()  # Create container if it doesn't exist
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(line_delimited_data, overwrite=True)
    print(f"Uploaded data to Blob Storage: {blob_name}")
