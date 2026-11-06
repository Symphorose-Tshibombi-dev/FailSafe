import csv, io
from pydantic import ValidationError
from .models import ClinicRecordIn
from .repository import create_record

REQUIRED={"clinic_code","reporting_date","department","metric","value","unit"}

def import_csv(content):
    reader=csv.DictReader(io.StringIO(content))
    if not reader.fieldnames:
        return {"imported":0,"rejected":0,"errors":[{"row":1,"error":"CSV header is missing"}]}
    missing=sorted(REQUIRED-set(reader.fieldnames))
    if missing:
        return {"imported":0,"rejected":0,"errors":[{"row":1,"error":"Missing columns: "+", ".join(missing)}]}
    imported=rejected=0
    errors=[]
    for number,row in enumerate(reader,start=2):
        try:
            record=ClinicRecordIn.model_validate(row)
            create_record(record.model_copy(update={"source":"csv"}))
            imported+=1
        except (ValidationError,ValueError,TypeError) as exc:
            rejected+=1
            errors.append({"row":number,"error":str(exc)})
    return {"imported":imported,"rejected":rejected,"errors":errors}
