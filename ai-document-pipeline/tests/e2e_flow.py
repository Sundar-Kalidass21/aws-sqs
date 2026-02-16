import requests
import time
import os

API_URL = "http://localhost:8000/api/v1/documents"

def test_pipeline():
    print("Starting End-to-End Test...")

    # 1. Create a dummy file
    filename = "test_doc.csv"
    with open(filename, "w") as f:
        f.write("col1,col2\nval1,val2")
    
    try:
        # 2. Upload file
        print(f"Uploading {filename}...")
        with open(filename, "rb") as f:
            response = requests.post(API_URL + "/", files={"file": f})
        
        if response.status_code != 200:
            print(f"Upload failed: {response.text}")
            return

        job = response.json()
        job_id = job["id"]
        print(f"Job created with ID: {job_id}. Initial status: {job['status']}")

        # 3. Poll status
        max_retries = 10
        for i in range(max_retries):
            time.sleep(2)
            print(f"Polling status (attempt {i+1})...")
            
            status_res = requests.get(f"{API_URL}/{job_id}")
            if status_res.status_code != 200:
                print(f"Status check failed: {status_res.text}")
                continue
            
            job_status = status_res.json()
            current_status = job_status["status"]
            print(f"Current status: {current_status}")

            if current_status == "COMPLETED":
                print("Job Completed Successfully!")
                print("Result:", job_status.get("result"))
                return
            
            if current_status == "FAILED":
                print("Job Failed!")
                return
        
        print("Timeout waiting for job completion.")

    finally:
        # Cleanup
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == "__main__":
    test_pipeline()
