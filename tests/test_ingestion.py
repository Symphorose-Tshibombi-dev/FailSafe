from failsafe.ingestion import import_csv

def test_missing_columns():
    result=import_csv("clinic_code,reporting_date\nCLINIC-01,2026-10-01\n")
    assert result["imported"]==0
    assert "Missing columns" in result["errors"][0]["error"]

def test_empty_csv():
    result=import_csv("")
    assert result["imported"]==0 and result["errors"][0]["row"]==1
