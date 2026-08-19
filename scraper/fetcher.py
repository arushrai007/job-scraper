import requests
from scraper.pacing import polite_delay

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
    from scraper.validator import validate_batch

    data = fetch_jobs()
    result = validate_batch(data["data"])

    print(f"Total jobs fetched: {result['total']}")
    print(f"Valid: {result['valid_count']}")
    print(f"Invalid: {result['invalid_count']}")

    if result["invalid_jobs"]:
        print("\nProblems found:")
        for item in result["invalid_jobs"]:
            print(f"  {item['job_slug']}: {item['problems']}")