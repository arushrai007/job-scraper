from flask import Flask, jsonify
from scraper.fetcher import fetch_jobs
from scraper.validator import validate_batch
from scraper.storage import save_jobs, load_existing_jobs
from scraper.logger import get_logger

app = Flask(__name__)
logger = get_logger()


@app.route("/")
def home():
    """Simple landing page confirming the service is up."""
    return jsonify({
        "service": "job-scraper-demo",
        "endpoints": {
            "/run": "Triggers a fresh pull from Arbeitnow",
            "/jobs": "Returns all currently stored jobs",
        }
    })


@app.route("/run")
def run_pipeline():
    """
    Triggers one pull from Arbeitnow, validates it, and stores results.
    Returns a JSON summary of what happened.
    """
    logger.info("Pipeline run triggered via /run endpoint")

    data = fetch_jobs()

    if data is None:
        logger.error("Pull failed after all retries")
        return jsonify({"status": "failed", "message": "Could not fetch data after retries"}), 502

    result = validate_batch(data["data"])
    storage_summary = save_jobs(result["valid_jobs"])

    logger.info(f"Run complete: {storage_summary}")

    return jsonify({
        "status": "success",
        "fetched": result["total"],
        "valid": result["valid_count"],
        "invalid": result["invalid_count"],
        "newly_added": storage_summary["added"],
        "already_known": storage_summary["already_known"],
        "total_stored": storage_summary["total_stored"],
    })


@app.route("/jobs")
def list_jobs():
    """Returns all jobs currently saved in storage."""
    jobs = load_existing_jobs()
    return jsonify({
        "total": len(jobs),
        "jobs": list(jobs.values())[:20],  # cap at 20 so the response isn't huge
    })


if __name__ == "__main__":
    app.run(debug=False)
