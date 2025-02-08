# NBADataLake
This repository contains:
- setup_nba_data_lake.py script, which orchestrates the workflow
- azure_resources.py, which creates the Azure resources dynamically
- data_operations.py, fetches data from the API and uploads it to Blob Storage
- .env, which contains your environment variables and shout be added to .gitignore

## **Project Structure**

## Project Folder Structure
- **AzureDataLake/**
    - `Instructions` → Folder with steps
      - `Instructions.md` → Documentation for the project
  - `.env` → Environment variables file
  - `setup_nba_data_lake.py` → Main script for setting up the data lake
  - `azure_resources.py` → Script for creating Azure resources
  - `data_operations.py` → Script for fetching data and uploading it
  - `requirements.txt` → Python dependencies
  - `.gitignore` → Ignores .env and Instructions folder

# AWS to Azure Translation

For those of you who previously completed the lab in AWS, here is a quick break down of how the services map to Azure:

- Azure Blob storage will be used to store the raw data instead of S3 in the AWS project. You will see functions like "create_blob_container" and "upload_to_blob_storage' that replace the S3 operations.
- Synapse Analytics replaces Glue and Athena to query the data, we can use SQL pools or Spark pools to accomplish this. Query step is a placeholder "query_with_synapse", sunce Synapse requires more extensive setup for execution.
- We have to include environment variables that are specific to Azure like the Azure_Storage_Account, Azure_Connection_String and Azure_Resource_Group


# Prerequisites
Before running the scripts, ensure you have the following:

## **1** Sportsdata.io Account

Go to Sportsdata.io and create a free account
At the top left, you should see "Developers", if you hover over it you should see "API Resources"
Click on "Introduction & Testing"

Click on "SportsDataIO API Free Trial" and fill out the information & be sure to select NBA for this tutorial

You will get an email and at the bottom it says "Launch Developer Portal"

By default it takes you to the NFL, on the left click on NBA

Scroll down until you see "Standings"

You'll "Query String Parameters", the value in the drop down box is your API key. 

Copy this string because you will need to paste it later in the script

## **2** Set up Azure Account
- [Azure $200 Credit](https://azure.microsoft.com/en-us/pricing/purchase-options/azure-account/search?ef_id=_k_Cj0KCQiA-5a9BhCBARIsACwMkJ67jIcqe3S-QU-D_O1aHxhjC1WkH61u0loQD0H5-tu3OJsRpoy8uz4aAnepEALw_wcB_k_&OCID=AIDcmm5edswduu_SEM__k_Cj0KCQiA-5a9BhCBARIsACwMkJ67jIcqe3S-QU-D_O1aHxhjC1WkH61u0loQD0H5-tu3OJsRpoy8uz4aAnepEALw_wcB_k_&gad_source=1&gclid=Cj0KCQiA-5a9BhCBARIsACwMkJ67jIcqe3S-QU-D_O1aHxhjC1WkH61u0loQD0H5-tu3OJsRpoy8uz4aAnepEALw_wcB)
- [Azure For Students](https://azure.microsoft.com/en-us/free/students)
- [Azure For Startups](https://www.microsoft.com/en-us/startups)

## **3** Install VS Code Extensions for Azure CLI/Bash
- Install Azure CLI Tools
- Install Azure Tools
- Install Azure Resources
- Comprehensive [list](https://code.visualstudio.com/docs/azure/overview) of VS Code Extensions for Azure 

## **4** Install Azure SDKs & Python Packages
Install Python
```bash
brew install python
```

```bash
python3 -m ensurepip --default-pip
```

```bash
pip install azure-identity azure-mgmt-resource azure-mgmt-storage azure-mgmt-synapse azure-storage-blob python-dotenv requests
```

- Install dependencies
```bash
   pip install -r requirements.txt
```

# START HERE 
# Step 1: Open VsCode

1. Sign into your Azure account, [video](https://www.youtube.com/watch?v=kAbKjr3geW4)/[documentation](https://code.visualstudio.com/docs/azure/gettingstarted#:~:text=Select%20the%20Azure%20icon%20in,services%20right%20from%20VS%20Code.) for help
2. Clone the repo
```bash
git clone [https://github.com/alahl1/SportsDataBackup](https://github.com/alahl1/Azure-30day--DevOps-Challenge)
cd Projects
cd Week1
cd AzureDataLake
```
# Step 2: Update the .env file
Add:
- Your Sports Data API Key
- Your Azure Subscription ID
- Create a unqiue Azure Resource Group Name
- Create a unique storage account name
- Create a unique synapse workspace name
- The Azure Connection String & Synapse SQL endpoint will be injected, leave this blank.
- Create an admin username

# Step 3: Run setup_nba_data_lake.py file
1.  In the Bash terminal, type
```bash
python setup_nba_data_lake.py
```

# Step 4: Manually Check For The Resources
Azre Portal
1. Navigate to the Storage Account by search for the name
2. Under the "Data Storage" section, click Containers
3. Check for the file "raw-data/nba_player_data.jsonl"

Use CLI 
List Blobs in the Container
```bash
az storage blob list --container-name nba-datalake --account-name <your_storage_account_name> --query "[].name" --output table
```

Download the File
```bash
az storage blob download --container-name nba-datalake --account-name <your_storage_account_name> --name raw-data/nba_player_data.jsonl --file nba_player_data.jsonl
```
View the contents
```bash
cat nba_player_data.jsonl
```

### **What We Learned**
1. Creating a data pipline with Azure Services
2. Automating Cloud Infrastructure with Python
3. Working with Json and Line-Delimited (JSONL)

### **Future Enhancements**
1. Automating data refresh with Azure Functions
2. Real time NBA stream with Azure Event Hubs
3. Connect Power BI to Synapse Analytics to create dashboards
4. Integrate Azure Key Vault for Credential Management
