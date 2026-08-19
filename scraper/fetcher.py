import requests
from scraper.pacing import polite_delay

ARBEITNOW_URL = "https://www.arbeitnow.com/api/job-board-api"

MAX_RETRIES = 3


def fetch_jobs():
    """
    Fetches job listings from Arbeitnow, retrying on failure with
    increasing backoff. Returns None if all retries are exhausted,
    instead of crashing the whole pipeline.
    """
    from scraper.logger import get_logger
    logger = get_logger()

    headers = {
        "User-Agent": "job-scraper-demo/0.1 (educational project; contact: your-email@example.com)"
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(ARBEITNOW_URL, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()

        except (requests.exceptions.RequestException, ValueError) as e:
            logger.warning(f"Attempt {attempt}/{MAX_RETRIES} failed: {e}")

            if attempt < MAX_RETRIES:
                backoff_seconds = attempt * 3
                logger.info(f"Retrying in {backoff_seconds}s...")
                import time
                time.sleep(backoff_seconds)
            else:
                logger.error("All retries exhausted. Giving up on this pull.")
                return None


if __name__ == "__main__":
    from scraper.validator import validate_batch
    from scraper.storage import save_jobs
    from scraper.logger import get_logger

    logger = get_logger()
    logger.info("Pipeline run started")

    for i in range(3):
        logger.info(f"--- Pull #{i+1} ---")
        data = fetch_jobs()

        if data is None:
            logger.error(f"Pull #{i+1} failed after all retries — no data returned")
            continue

        result = validate_batch(data["data"])
        logger.info(f"Total: {result['total']}, Valid: {result['valid_count']}, Invalid: {result['invalid_count']}")

        if result["invalid_count"] > 0:
            logger.warning(f"{result['invalid_count']} jobs failed schema validation — possible source change")

        storage_summary = save_jobs(result["valid_jobs"])
        logger.info(
            f"Storage: {storage_summary['added']} new, "
            f"{storage_summary['already_known']} already known, "
            f"{storage_summary['total_stored']} total stored"
        )

        if i < 2:
            polite_delay()

    logger.info("Pipeline run finished")