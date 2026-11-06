from fastapi.testclient import TestClient
from failsafe.main import app
client=TestClient(app)

def payload(value=42):
    return {"clinic_code":"CLINIC-01","reporting_date":"2026-10-01",
            "department":"Outpatient","metric":"visits","value":value,"unit":"visits"}

def test_health():
    response=client.get("/health")
    assert response.status_code==200 and response.json()["status"]=="ok"

def test_create_and_retrieve():
    created=client.post("/records",json=payload())
    assert created.status_code==201
    record=client.get("/records/"+created.json()["record_id"])
    assert record.status_code==200 and record.json()["value"]==42
    assert record.json()["sync_status"]=="pending"

def test_negative_value_rejected():
    assert client.post("/records",json=payload(-1)).status_code==422

def test_csv_import_reports_bad_rows():
    csv=("clinic_code,reporting_date,department,metric,value,unit\n"
         "CLINIC-01,2026-10-01,Outpatient,visits,12,visits\n"
         "CLINIC-01,not-a-date,Outpatient,visits,5,visits\n")
    result=client.post("/ingest/csv",content=csv,headers={"content-type":"text/csv"})
    assert result.status_code==200
    assert result.json()["imported"]==1 and result.json()["rejected"]==1

def test_analytics():
    client.post("/records",json=payload(10))
    result=client.get("/analytics/summary")
    assert result.status_code==200 and result.json()[0]["total_value"]==10

def test_sync_acknowledgement():
    item=client.post("/records",json=payload()).json()
    assert len(client.get("/sync/pending").json())==1
    ack=client.post("/sync/acknowledge",json={"record_ids":[item["record_id"]]})
    assert ack.json()["acknowledged"]==1
    assert client.get("/sync/pending").json()==[]
