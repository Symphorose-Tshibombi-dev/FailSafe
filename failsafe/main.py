from fastapi import FastAPI

app = FastAPI(
    title="FailSafe Clinic Data API",
    description=(
        "An offline-first prototype for collecting, validating, storing, "
        "and sharing rural clinic data."
    ),
    version="0.1.0",
)


@app.get("/health", tags=["Operations"])
def health_check() -> dict[str, str]:
    """Report whether the API process is responding."""
    return {"status": "ok", "service": "FailSafe"}
