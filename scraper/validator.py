
EXPECTED_SCHEMA = {
    "slug": str,
    "company_name": str,
    "title": str,
    "description": str,
    "remote": bool,
    "url": str,
    "tags": list,
    "job_types": list,
    "location": str,
    "created_at": int,
}


def validate_job(job: dict) -> list:
    """
    Checks a single job dict against EXPECTED_SCHEMA.
    Returns a list of problem strings. Empty list = job is valid.
    """
    problems = []

    for field, expected_type in EXPECTED_SCHEMA.items():
        if field not in job:
            problems.append(f"Missing field: '{field}'")
            continue

        if not isinstance(job[field], expected_type):
            actual_type = type(job[field]).__name__
            problems.append(
                f"Wrong type for '{field}': expected {expected_type.__name__}, got {actual_type}"
            )

    return problems


def validate_batch(jobs: list) -> dict:
    """
    Validates a list of job dicts.
    Returns a summary: how many passed, how many failed, and details on failures.
    """
    valid_jobs = []
    invalid_jobs = []

    for job in jobs:
        problems = validate_job(job)
        if problems:
            invalid_jobs.append({"job_slug": job.get("slug", "UNKNOWN"), "problems": problems})
        else:
            valid_jobs.append(job)

    return {
        "total": len(jobs),
        "valid_count": len(valid_jobs),
        "invalid_count": len(invalid_jobs),
        "valid_jobs": valid_jobs,
        "invalid_jobs": invalid_jobs,
    }