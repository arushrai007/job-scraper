# Job Scraper

A lightweight job ingestion service that fetches publicly available job listings, validates the incoming data, removes duplicates, and stores the results for later retrieval.

The project focuses on building a reliable ingestion pipeline with failure handling and bounded retries without attempting to bypass access controls or restrictions on job platforms.

## Features

- Fetches job listings from the public Arbeitnow Job Board API
- Validates incoming job records before storing them
- Handles temporary source and network failures with bounded retries
- Uses increasing delays between retry attempts
- Avoids storing duplicate job listings
- Persists previously collected jobs
- Provides API endpoints for triggering ingestion and retrieving jobs
- Structured logging for ingestion activity
- Graceful failure when the source cannot be reached

## Architecture

```text
                    ┌─────────────────────┐
                    │   Arbeitnow API     │
                    │  Public Job Source  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       Fetcher       │
                    │ HTTP + Retry/Backoff│
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Validator      │
                    │ Check job structure │
                    │   and required data │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       Storage       │
                    │ Deduplication +     │
                    │ Persistent Storage  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Flask API      │
                    │                     │
                    │ /run                │
                    │ /jobs               │
                    │ /                   │
                    └─────────────────────┘
```

## Tech Stack

- **Python**
- **Flask** — web application and API endpoints
- **Requests** — HTTP communication with the job source
- **Arbeitnow Job Board API** — public job data source
- **Git/GitHub** — version control
- **Render** — deployment

## Project Structure

```text
job-scraper/
│
├── app.py
├── requirements.txt
├── README.md
├── DECISIONS.md
│
└── scraper/
    ├── fetcher.py
    ├── validator.py
    ├── storage.py
    └── logger.py
```

## How the Pipeline Works

The ingestion process follows these steps:

```text
1. Trigger ingestion
        ↓
2. Request data from Arbeitnow
        ↓
3. Retry temporary failures
        ↓
4. Validate received job records
        ↓
5. Ignore invalid records
        ↓
6. Check for existing jobs
        ↓
7. Store new jobs
        ↓
8. Return ingestion summary
```

### 1. Fetch

The fetcher sends an HTTP request to the public Arbeitnow job API.

If the request fails because of a temporary network or source problem, the system retries a limited number of times with increasing delays.

The system does not attempt to bypass source restrictions or continuously request an unavailable source.

### 2. Validate

The received records are checked before they are stored.

Invalid or incomplete records are excluded from the final dataset.

### 3. Deduplicate

Previously stored jobs are identified so that repeated ingestion runs do not continuously create duplicate records.

### 4. Store

Valid, previously unseen jobs are persisted in storage.

Existing jobs remain available even if a later ingestion attempt fails.

## API Endpoints

### `GET /`

Returns basic information about the service and available endpoints.

### `GET /run`

Triggers a new ingestion run.

A successful response contains information such as:

```json
{
    "status": "success",
    "fetched": 175,
    "valid": 175,
    "invalid": 0,
    "newly_added": 0,
    "already_known": 175,
    "total_stored": 175
}
```

The exact values depend on the current source data and previously stored jobs.

### `GET /jobs`

Returns the currently stored jobs.

The response includes the total number of stored jobs and a limited number of job records.

## Failure Handling

A key part of the system is handling source failures safely.

If the source temporarily fails:

```text
Request
   ↓
Failure
   ↓
Retry
   ↓
Increasing delay
   ↓
Retry
   ↓
Retry limit reached
   ↓
Graceful failure
```

The system uses bounded retries rather than continuously requesting the source.

If all retries fail, the ingestion run returns a failure response instead of crashing the application.

## Data Integrity

The ingestion process separates:

- Fetching
- Validation
- Storage

This prevents invalid source data from being directly written into storage.

The pipeline also tracks:

- Total records fetched
- Valid records
- Invalid records
- Newly added records
- Already known records
- Total stored records

## Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/arushrai007/job-scraper/
cd job-scraper
```

### 2. Create a virtual environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the application

```bash
python app.py
```

The application will be available at:

```text
http://127.0.0.1:5000
```

## Deployment

The application is deployed using Render.

Live deployment:

https://job-scraper-aasw.onrender.com/

## Design Decisions

Important engineering decisions and their reasoning are documented separately in:

```text
DECISIONS.md
```

The document covers:

- Why the selected job source was used
- How the system behaves when the source becomes unavailable
- What would be changed for a larger production-scale system

## Limitations

This is a focused ingestion demonstration rather than a production-scale job aggregation platform.

Current limitations include:

- A single job source is currently used
- The ingestion process is manually triggered
- The current API response exposes a limited number of stored jobs
- There is no authentication or user-management layer

These choices keep the implementation focused on ingestion, validation, storage, and resilience.

## Future Improvements

If this system were expanded, possible improvements would include:

- Multiple independent source adapters
- Scheduled ingestion
- More robust persistent database infrastructure
- Source-specific rate limiting
- Monitoring and alerting
- More detailed ingestion history
- Job search and filtering
- Pagination
- Automated integration tests
- Better observability and metrics

## Author

**Arush Rai**

Built as a job ingestion system demonstration.
