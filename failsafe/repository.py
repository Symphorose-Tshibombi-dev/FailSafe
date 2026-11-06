from uuid import uuid4
from .database import get_connection
from .models import ClinicRecordIn

def create_record(record: ClinicRecordIn):
    values = record.model_dump(mode="json")
    record_id = str(uuid4())
    with get_connection() as db:
        db.execute("""INSERT INTO clinic_records
        (record_id,clinic_code,reporting_date,department,metric,value,unit,source)
        VALUES (?,?,?,?,?,?,?,?)""",
        (record_id,values["clinic_code"],values["reporting_date"],values["department"],
         values["metric"],values["value"],values["unit"],values["source"]))
        row = db.execute("SELECT * FROM clinic_records WHERE record_id=?",(record_id,)).fetchone()
    return dict(row)

def get_record(record_id):
    with get_connection() as db:
        row=db.execute("SELECT * FROM clinic_records WHERE record_id=?",(record_id,)).fetchone()
    return dict(row) if row else None

def list_records(clinic_code=None,limit=100,offset=0):
    sql="SELECT * FROM clinic_records"
    params=[]
    if clinic_code:
        sql+=" WHERE clinic_code=?"
        params.append(clinic_code)
    sql+=" ORDER BY reporting_date DESC,created_at DESC LIMIT ? OFFSET ?"
    params.extend([limit,offset])
    with get_connection() as db:
        return [dict(r) for r in db.execute(sql,params).fetchall()]

def aggregate_summary(clinic_code=None):
    sql="""SELECT clinic_code,department,metric,COUNT(*) record_count,
    SUM(value) total_value,AVG(value) average_value FROM clinic_records"""
    params=[]
    if clinic_code:
        sql+=" WHERE clinic_code=?"
        params.append(clinic_code)
    sql+=" GROUP BY clinic_code,department,metric ORDER BY clinic_code,department,metric"
    with get_connection() as db:
        return [dict(r) for r in db.execute(sql,params).fetchall()]

def pending_records(limit=500):
    with get_connection() as db:
        return [dict(r) for r in db.execute(
          "SELECT * FROM clinic_records WHERE sync_status='pending' ORDER BY created_at LIMIT ?",
          (limit,)).fetchall()]

def acknowledge_records(record_ids):
    marks=",".join("?" for _ in record_ids)
    with get_connection() as db:
        cur=db.execute(f"UPDATE clinic_records SET sync_status='synced' WHERE record_id IN ({marks})",record_ids)
        return cur.rowcount

def record_count():
    with get_connection() as db:
        return db.execute("SELECT COUNT(*) FROM clinic_records").fetchone()[0]
