import os
from dotenv import load_dotenv

# Force reloading environment variables from .env, even if they were already set.
load_dotenv(override=True)

###################################
# RapidAPI & Fetch-Related Config
###################################
API_URL = os.getenv("API_URL", "https://sport-highlights-api.p.rapidapi.com/basketball/highlights")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST", "sport-highlights-api.p.rapidapi.com")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
DATE = os.getenv("DATE", "2023-12-01")
LEAGUE_NAME = os.getenv("LEAGUE_NAME", "NCAA")
LIMIT = int(os.getenv("LIMIT", "10"))

###################################
# Azure Blob Storage Settings
###################################
AZURE_SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID")
AZURE_RESOURCE_GROUP = os.getenv("AZURE_RESOURCE_GROUP")
AZURE_LOCATION = os.getenv("AZURE_LOCATION", "eastus")
AZURE_STORAGE_ACCOUNT_NAME = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
AZURE_STORAGE_ACCOUNT_KEY = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")
AZURE_BLOB_CONTAINER_NAME = os.getenv("AZURE_BLOB_CONTAINER_NAME")

# Build the connection string if not explicitly set.
AZURE_STORAGE_CONNECTION_STRING = os.getenv(
    "AZURE_STORAGE_CONNECTION_STRING",
    f"DefaultEndpointsProtocol=https;AccountName={AZURE_STORAGE_ACCOUNT_NAME};AccountKey={AZURE_STORAGE_ACCOUNT_KEY};EndpointSuffix=core.windows.net"
)

###################################
# Video Paths in Blob Storage
###################################
INPUT_KEY = os.getenv("INPUT_KEY", "highlights/basketball_highlights.json")
OUTPUT_KEY = os.getenv("OUTPUT_KEY", "videos/first_video.mp4")

###################################
# Retry/Delay Configuration for run_all.py
###################################
RETRY_COUNT = int(os.getenv("RETRY_COUNT", "3"))
RETRY_DELAY = int(os.getenv("RETRY_DELAY", "30"))
WAIT_TIME_BETWEEN_SCRIPTS = int(os.getenv("WAIT_TIME_BETWEEN_SCRIPTS", "60"))
