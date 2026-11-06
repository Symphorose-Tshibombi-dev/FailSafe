# FailSafe

WTC-MKDTX8Y5

## Overview

FailSafe is an offline-first rural clinic data engineering prototype. It is
intended to help a clinic collect and validate operational data when internet
connectivity is unreliable, store that data locally, and make it available to
other services through a documented API.

This repository is being developed incrementally. The current foundation is
a small FastAPI application with a health-check endpoint and an automated
test. The data ingestion, SQLite persistence, offline workflow, and HealthSafe
integration are planned milestones, not features claimed as complete.

## Project goals

- Accept structured clinic data using a clearly defined schema.
- Validate and clean incoming records before storing them.
- Persist records locally with SQLite so basic clinic workflows do not depend
  on a live internet connection.
- Expose data through REST endpoints with JSON responses.
- Provide a later synchronisation boundary for connectivity-restored workflows.
- Demonstrate integration with the separate HealthSafe project through APIs.

## Current implementation

- FastAPI application in `failsafe/main.py`.
- `GET /health` endpoint for a basic service health check.
- Automated endpoint test in `tests/test_health.py`.

## Planned architecture

1. **Data model:** define the clinic records and validation rules.
2. **Ingestion:** accept sample CSV data and report invalid rows.
3. **Persistence:** store valid records in a local SQLite database.
4. **API:** retrieve stored records as JSON.
5. **Offline behaviour:** prove that locally stored records remain available
   without network access.
6. **Integration:** allow HealthSafe to consume selected data through the API.
7. **Synchronisation prototype:** define and test how locally captured records
   could be queued for later synchronisation.

## Technology

- Python 3.11+
- FastAPI
- SQLite (planned for the persistence milestone)
- Pytest and HTTPX

## Run locally

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the API:

```bash
uvicorn failsafe.main:app --reload
```

Open the interactive API documentation at `http://127.0.0.1:8000/docs`.
Check the service at `http://127.0.0.1:8000/health`.

Run automated tests:

```bash
pytest
```

## Data and safety note

This is a learning prototype, not a production clinical system. Use synthetic
or appropriately de-identified data only. It is not intended to store real
patient-identifiable or clinical information.

## Development history

Work is organised into small feature branches and meaningful commits. Each
milestone should include tests and documentation before it is merged into
`main`.
