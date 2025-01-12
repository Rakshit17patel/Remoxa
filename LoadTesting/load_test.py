import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

URL = "URL_HERE"
IMAGE_PATH = "./PATH_HERE"
NUM_REQUESTS = 20
CONCURRENT_WORKERS = 2

def send_request(session, url, image_path, retry=3):
    with open(image_path, 'rb') as img:
        files = {'image': img}
        for attempt in range(retry):
            try:
                response = session.post(url, files=files, timeout=10)
                return response.status_code
            except requests.exceptions.RequestException as e:
                print(f"Attempt {attempt+1}: Request failed: {e}")
                time.sleep(1)  # Wait before retrying
    return None

def main():
    start_time = time.time()
    success = 0
    failures = 0
    with ThreadPoolExecutor(max_workers=CONCURRENT_WORKERS) as executor:
        with requests.Session() as session:
            futures = [
                executor.submit(send_request, session, URL, IMAGE_PATH)
                for _ in range(NUM_REQUESTS)
            ]
            for future in as_completed(futures):
                status = future.result()
                if status and 200 <= status < 300:
                    print(f"Request completed with status code: {status}")
                    success += 1
                else:
                    print(f"Request failed with status code: {status}")
                    failures += 1
    end_time = time.time()
    print(f"Completed {NUM_REQUESTS} requests in {end_time - start_time:.2f} seconds.")
    print(f"Successful requests: {success}")
    print(f"Failed requests: {failures}")

if __name__ == "__main__":
    main()
