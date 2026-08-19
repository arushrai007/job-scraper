import requests

ARBEITNOW_URL = "https://www.arbeitnow.com/api/job-board-api"

def fetch_jobs():
    """
    Fetches the latest job listings from Arbeitnow's public API.
    Returns the raw JSON response as a Python dict.
    """
    headers = {
        "User-Agent": "job-scraper-demo/0.1 (educational project; contact: your-email@example.com)"
    }

    response = requests.get(ARBEITNOW_URL, headers=headers, timeout=10)
    response.raise_for_status()  # throws an error if status code is 4xx/5xx

    return response.json()


if __name__ == "__main__":
    data = fetch_jobs()
    print(f"Fetched {len(data['data'])} jobs")
    print("First job example:")
    print(data['data'][0])