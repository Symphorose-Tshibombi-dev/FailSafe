from datetime import date
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator

class ClinicRecordIn(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    clinic_code: str = Field(min_length=2, max_length=30, pattern=r"^[A-Za-z0-9_-]+$")
    reporting_date: date
    department: str = Field(min_length=2, max_length=80)
    metric: str = Field(min_length=2, max_length=80)
    value: float = Field(ge=0, le=1000000000)
    unit: str = Field(min_length=1, max_length=30)
    source: str = Field(default="api", min_length=1, max_length=40)

    @field_validator("department", "metric", "unit", "source")
    @classmethod
    def nonblank(cls, value):
        if not value.strip():
            raise ValueError("must not be blank")
        return value

class ClinicRecord(ClinicRecordIn):
    record_id: str
    sync_status: Literal["pending", "synced"]
    created_at: str

class ImportResult(BaseModel):
    imported: int
    rejected: int
    errors: list[dict]

class SyncAcknowledgement(BaseModel):
    record_ids: list[str] = Field(min_length=1, max_length=500)

class SummaryItem(BaseModel):
    clinic_code: str
    department: str
    metric: str
    record_count: int
    total_value: float
    average_value: float
