from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query, Request
from .database import initialise_database
from .ingestion import import_csv
from .models import ClinicRecord, ClinicRecordIn, ImportResult, SummaryItem, SyncAcknowledgement
from .repository import (acknowledge_records,aggregate_summary,create_record,
                          get_record,list_records,pending_records,record_count)

@asynccontextmanager
async def lifespan(_: FastAPI):
    initialise_database()
    yield

app=FastAPI(title="FailSafe Clinic Data API",
 description="Offline-first prototype for aggregate rural clinic operational data.",
 version="1.0.0",lifespan=lifespan)

@app.get("/health",tags=["Operations"])
def health():
    return {"status":"ok","service":"FailSafe","records":record_count()}

@app.post("/records",response_model=ClinicRecord,status_code=201,tags=["Clinic records"])
def add_record(payload: ClinicRecordIn):
    return create_record(payload)

@app.get("/records",response_model=list[ClinicRecord],tags=["Clinic records"])
def get_records(clinic_code: str|None=None,limit:int=Query(100,ge=1,le=500),offset:int=Query(0,ge=0)):
    return list_records(clinic_code,limit,offset)

@app.get("/records/{record_id}",response_model=ClinicRecord,tags=["Clinic records"])
def get_one_record(record_id:str):
    record=get_record(record_id)
    if not record:
        raise HTTPException(status_code=404,detail="Clinic record not found")
    return record

@app.post("/ingest/csv",response_model=ImportResult,tags=["Data ingestion"])
async def ingest_csv(request:Request):
    if not any(x in request.headers.get("content-type","") for x in ("text/csv","text/plain")):
        raise HTTPException(status_code=415,detail="Send CSV using text/csv or text/plain")
    try:
        content=(await request.body()).decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=400,detail="CSV must be UTF-8 encoded") from exc
    return import_csv(content)

@app.get("/analytics/summary",response_model=list[SummaryItem],tags=["Analytics"])
def summary(clinic_code:str|None=None):
    return aggregate_summary(clinic_code)

@app.get("/sync/pending",response_model=list[ClinicRecord],tags=["HealthSafe integration"])
def sync_pending(limit:int=Query(500,ge=1,le=500)):
    return pending_records(limit)

@app.post("/sync/acknowledge",tags=["HealthSafe integration"])
def sync_acknowledge(payload:SyncAcknowledgement):
    return {"acknowledged":acknowledge_records(payload.record_ids),"requested":len(payload.record_ids)}

@app.get("/",tags=["Operations"])
def root():
    return {"service":"FailSafe","version":app.version,"docs":"/docs"}
