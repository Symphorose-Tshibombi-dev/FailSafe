# FailSafe

WTC-MKDTX8Y5

## Overview
FailSafe is an offline-first rural clinic data engineering prototype. It
collects aggregate clinic operational metrics, validates them, stores them in
a local SQLite database, provides analytics, and exposes a pull-based
synchronisation interface for connected systems such as HealthSafe.

This is a learning prototype, not a production clinical system. Use synthetic
or de-identified aggregate data only. Do not submit patient names, identity
numbers, contact details, diagnoses, or other identifiable health information.

## Features
- FastAPI REST API and interactive OpenAPI documentation.
- SQLite local persistence; writing records does not require internet access.
- Pydantic validation for clinic codes, dates, text and non-negative metrics.
- CSV ingestion with row-level validation and rejected-row reporting.
- Filtering and pagination for stored records.
- SQL analytics grouped by clinic, department and metric.
- Pending-sync queue for HealthSafe to pull and acknowledge.
- Pytest suite and GitHub Actions test workflow.
- Synthetic sample dataset at data/sample_clinic_metrics.csv.

## Architecture
    CSV / local clinic capture
              |
              v
          FastAPI API
              |
       Pydantic validation
              |
              v
       SQLite local database
          |           |
          v           v
       Analytics   Pending sync queue
                       |
                connectivity returns
                       |
                       v
              HealthSafe pulls records

FailSafe owns its database. HealthSafe integrates through the API and must not
connect directly to the SQLite file. HealthSafe should acknowledge records
only after successfully processing them.

## Technology
Python 3.11+, FastAPI, Pydantic, SQLite, Pytest and HTTPX.

## Setup
    git clone https://github.com/Symphorose-Tshibombi-dev/FailSafe.git
    cd FailSafe
    git switch feature/project-foundation
    python -m venv .venv

Windows PowerShell:
    .venv\Scripts\Activate.ps1

macOS/Linux:
    source .venv/bin/activate

Install and run:
    pip install -r requirements.txt
    uvicorn failsafe.main:app --reload

Open http://127.0.0.1:8000/docs for API documentation. The default database
is data/failsafe.db. Set FAILSAFE_DB_PATH to select another local database.

## API reference
| Method | Endpoint | Purpose |
|---|---|---|
| GET | /health | Service status and record count |
| POST | /records | Validate and store one aggregate metric |
| GET | /records | List records; optional clinic_code, limit, offset |
| GET | /records/{record_id} | Retrieve one record |
| POST | /ingest/csv | Import CSV sent as text/csv |
| GET | /analytics/summary | Aggregate by clinic, department and metric |
| GET | /sync/pending | Records awaiting HealthSafe synchronisation |
| POST | /sync/acknowledge | Mark received record IDs as synchronised |

Example record:
    {
      "clinic_code": "CLINIC-001",
      "reporting_date": "2026-10-01",
      "department": "Outpatient",
      "metric": "visits",
      "value": 68,
      "unit": "visits"
    }

Import the sample CSV by sending its contents as the raw body to POST
/ingest/csv with Content-Type: text/csv. The response includes imported and
rejected row counts and row-level errors. Valid rows are retained even when
another row is rejected.

## HealthSafe synchronisation handshake
1. HealthSafe requests GET /sync/pending when connectivity is available.
2. HealthSafe validates and stores the returned records in its own system.
3. After successful processing, HealthSafe posts accepted record_ids to
   /sync/acknowledge.
4. Unacknowledged records remain pending and can be requested again.

This is a prototype contract, not a secure production sync protocol.
Authentication, encryption configuration, conflict resolution, retry backoff,
audit controls and deployment hardening remain future work.

## Tests
Run pytest. Tests use a temporary SQLite database and do not write into the
working database.

## Limitations and safety
- Sample data is synthetic and contains no patient identities.
- Offline data remains local until a connected system pulls it.
- No automatic network transfer occurs while offline.
- Not suitable for clinical decisions or production patient data.
- WTC-MKDTX8Y5 is the original verification code and is preserved.

## Development status
The implementation is on feature/project-foundation. The main branch remains
unchanged until local verification and review are complete.
