# process_one_video.py

import json
import requests
from io import BytesIO
from config import (
    AZURE_STORAGE_CONNECTION_STRING,
    AZURE_BLOB_CONTAINER_NAME,
    INPUT_KEY,
    OUTPUT_KEY
)
from azure.storage.blob import BlobServiceClient

def process_one_video():
    try:
        # Create the BlobServiceClient using the connection string.
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
        # Ensure the container name is lowercase.
        container_client = blob_service_client.get_container_client(AZURE_BLOB_CONTAINER_NAME.lower())
        
        print("Fetching JSON file from Azure Blob Storage...")
        # Download the JSON file using the input key.
        blob_client = container_client.get_blob_client(INPUT_KEY)
        download_stream = blob_client.download_blob()
        json_content = download_stream.readall().decode('utf-8')
        highlights = json.loads(json_content)
        
        # Extract the video URL from the JSON (adjust key as needed).
        video_url = highlights["data"][0]["url"]
        print(f"Processing video URL: {video_url}")
        
        print("Downloading video...")
        # Download the video from the external URL.
        video_response = requests.get(video_url, stream=True)
        video_response.raise_for_status()
        video_data = BytesIO(video_response.content)
        
        print("Uploading video to Azure Blob Storage...")
        # Upload the video file to Blob Storage using the output key.
        output_blob_client = container_client.get_blob_client(OUTPUT_KEY)
        output_blob_client.upload_blob(video_data, overwrite=True)
        print(f"Video uploaded successfully: {AZURE_BLOB_CONTAINER_NAME}/{OUTPUT_KEY}")
    except Exception as e:
        print(f"Error during video processing: {e}")

if __name__ == "__main__":
    process_one_video()
