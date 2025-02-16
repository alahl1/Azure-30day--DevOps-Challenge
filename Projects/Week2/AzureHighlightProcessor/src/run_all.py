# run_all.py

import subprocess
import time
from config import RETRY_COUNT, RETRY_DELAY, WAIT_TIME_BETWEEN_SCRIPTS

def run_script(script_name, retries=RETRY_COUNT, delay=RETRY_DELAY):
    attempt = 0
    while attempt < retries:
        try:
            print(f"Running {script_name} (attempt {attempt + 1}/{retries})...")
            subprocess.run(["python", script_name], check=True)
            print(f"{script_name} completed successfully.")
            return
        except subprocess.CalledProcessError as e:
            print(f"Error running {script_name}: {e}")
            attempt += 1
            if attempt < retries:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print(f"{script_name} failed after {retries} attempts.")
                raise e

def main():
    try:
        # Step 1: Create storage account and update .env
        run_script("create_storage_account.py")
        print("Waiting for resources to stabilize...")
        time.sleep(WAIT_TIME_BETWEEN_SCRIPTS)
        
        # Step 2: Fetch highlights and save JSON to Blob Storage
        run_script("fetch.py")
        print("Waiting for resources to stabilize...")
        time.sleep(WAIT_TIME_BETWEEN_SCRIPTS)
        
        # Step 3: Process one video (download JSON, download video, and upload video)
        run_script("process_one_video.py")
        print("All scripts executed successfully.")
    except Exception as e:
        print(f"Pipeline failed: {e}")

if __name__ == "__main__":
    main()
