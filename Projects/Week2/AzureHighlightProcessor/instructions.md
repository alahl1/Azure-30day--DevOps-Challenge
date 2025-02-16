#AzureGameHighlightProcessor

# HighlightProcessor
This project uses RapidAPI to obtain NCAA game highlights, stores the json file in an Azure Blob and then parses the json file for a video url and downloads the video to the same Azure Storage Blob.

# File Overview

The config.py script performs the following actions:
Loads environment variables from .env and provies configuration values for other scripts.

create_storage_account.py
Ensures that Azure resources exist before running the rest of the pipeline:
- Creates a resource group if it doesn't exisit
- Creates a storage account dynamically
- Retrieves the storage account key and updates the .env file

It connects to Azure using the Azure Resource Manager (ARM API) to provision the resources.

The fetch.py script performs the following actions:

Fetches basketball highlights from the RapidAPI Sports API and saves the JSON data to Azure Blob Storage.
This JSON data has highilight data and video urls.

process_one_video.py performs the following actions:

- Extracts the first videoURL from the JSON file
- Fetches the video from the external website
- Downloads and saves the video back to Azure Blob Storage

run_all.py performs the following actions:
Orchestrates the entire workflow, ensuring each step runs in sequence with retry logic.

.env file stores all over the environment variables, these are variables that we don't want to hardcode into our script.

Dockerfile performs the following actions:
Provides the step by step approach to build the image.

# Prerequisites
Before running the scripts, ensure you have the following:

## **1** Create Rapidapi Account
Rapidapi.com account, will be needed to access highlight images and videos.

For this example we will be using NCAA (USA College Basketball) highlights since it's included for free in the basic plan.

[Sports Highlights API](https://rapidapi.com/highlightly-api-highlightly-api-default/api/sport-highlights-api/playground/apiendpoint_16dd5813-39c6-43f0-aebe-11f891fe5149) is the endpoint we will be using 

## **2** Verify prerequites are installed 

Python3 should be pre-installed also python3 --version

Git - Cloning the repo

Set up Azure Account
- [Azure $200 Credit](https://azure.microsoft.com/en-us/pricing/purchase-options/azure-account/search?ef_id=_k_Cj0KCQiA-5a9BhCBARIsACwMkJ67jIcqe3S-QU-D_O1aHxhjC1WkH61u0loQD0H5-tu3OJsRpoy8uz4aAnepEALw_wcB_k_&OCID=AIDcmm5edswduu_SEM__k_Cj0KCQiA-5a9BhCBARIsACwMkJ67jIcqe3S-QU-D_O1aHxhjC1WkH61u0loQD0H5-tu3OJsRpoy8uz4aAnepEALw_wcB_k_&gad_source=1&gclid=Cj0KCQiA-5a9BhCBARIsACwMkJ67jIcqe3S-QU-D_O1aHxhjC1WkH61u0loQD0H5-tu3OJsRpoy8uz4aAnepEALw_wcB)
- [Azure For Students](https://azure.microsoft.com/en-us/free/students)
- [Azure For Startups](https://www.microsoft.com/en-us/startups)

## **3** Retrieve Azure Account ID

After logging in, you can run:
```bash
az account show --query id -o tsv
```
in the CLI to return the subscription id.

## **Project Structure**
```bash
src/
├── Dockerfile
├── config.py
├── fetch.py
├── create_storage_account.py
├── process_one_video.py
├── requirements.txt
├── run_all.py
├── .env
├── .gitignore
```
![AzureHighlightProcessor (1)](https://github.com/user-attachments/assets/7dff7f2c-4386-4f22-ab64-c7e0a5b06895)

# AWS to Azure Translation

For those of you who previously completed the lab in AWS, here is a quick break down of how the services map to Azure:
Azure Blob Storage replaces Amazon S3 for storing both highlight metadata(JSON) and processed videos.
Authentication now uses DefaultAzureCredential(), which works with Microsoft Entra ID instead of IAM roles.
AWS MediaConvert functionality that enhances the video/audio quality was removed since Azzure Media Services was deprecated in 2023.

| **AWS Service**                              | **Azure Service**                         | **Purpose** |
|----------------------------------------------|---------------------------------------------|-------------|
| Amazon S3 (Simple Storage Service)          | Azure Blob Storage                         | Stores highlight JSON data and processed video files. |
| IAM (Identity & Access Management)          | Microsoft Entra ID (formerly Azure AD)     | Provides secure authentication and access control. |
| AWS Lambda (for automation)                 | Azure Functions (not yet implemented)      | Could be used for event-driven automation in future enhancements. |
| AWS MediaConvert (for video processing)     | No equivalent (Removed)                    | Originally used for enhancing audio/visual quality, but Azure Media Services has been deprecated, so this step was removed. |


# START HERE - Local
## **Step 1: Clone The Repo**
```bash
git clone https://github.com/alahl1/Azure-30day--DevOps-Challenge/tree/main/Projects/Week2/AzureHighlightProcessor
cd src
```
## **Step 2: Update .env file**
1. RAPIDAPI_KEY
2. AZURE_SUBSCRIPTION_ID
3. AZURE_RESOURCE_GROUP
4. AZURE_BLOB_CONTAINER_NAME

## **Step 3: Secure .env file**
```bash
chmod 600 .env
```

## **Step 4: Setup Python Virtual Environment**
macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

Windows
```bash
python -m venv venv
venv\Scripts\activate
```

## **Step 5: Install Project Dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## **Step 6: Locally Run The Project**
Run:
```bash
python run_all.py
```
           
This will first excute create_storage_account.py, based on your wait_time_between_scripts settings it will wait a few seconds.
Next it runs fetch.py to fetch the highlights from RapidAPI and uploads the JSON file to the Blob Storage.
Finally it will run process_one_video.py to download the JSON file and process the video URL, download the video and upload it back to Blob Storage.

Optional - Confirm there is a JSON file is uploaded to the container
Optional - Confirm there is a video uploaded to the container

### **What We Learned**
1. 

### **Future Enhancements**
1. 
