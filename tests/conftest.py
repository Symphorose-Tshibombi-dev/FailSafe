import pytest

@pytest.fixture(autouse=True)
def isolated_database(tmp_path,monkeypatch):
    monkeypatch.setenv("FAILSAFE_DB_PATH",str(tmp_path/"test.db"))
    from failsafe.database import initialise_database
    initialise_database()
