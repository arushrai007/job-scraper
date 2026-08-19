import json
import os

DATA_FILE = "data.json"


def load_existing_jobs() -> dict:
    """
    Loads previously saved jobs from disk.
    Returns a dict keyed by 'slug' for fast lookup.
    If no file exists yet, returns an empty dict.
    """
    if not os.path.exists(DATA_FILE):
        return {}

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            jobs_list = json.load(f)
        except json.JSONDecodeError:
            # File exists but is empty or corrupted — treat as no data
            return {}

    # Convert list back into a dict keyed by slug for fast lookup
    return {job["slug"]: job for job in jobs_list}


def save_jobs(new_jobs: list) -> dict:
    """
    Merges new_jobs into existing storage, deduplicating by 'slug'.
    Returns a summary: how many were newly added vs already known.
    """
    existing = load_existing_jobs()

    added_count = 0
    for job in new_jobs:
        slug = job["slug"]
        if slug not in existing:
            existing[slug] = job
            added_count += 1

    # Write the merged dict back to disk as a list
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(list(existing.values()), f, indent=2)

    return {
        "added": added_count,
        "already_known": len(new_jobs) - added_count,
        "total_stored": len(existing),
    }