import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.setup_database.models import Base, AirPollutionData

# Create a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Dependency override
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_main_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "<h1>Welcome to Air Pollution Data Viewer</h1>" in response.text
    assert "<form action=\"/get_stats/\" method=\"post\">" in response.text
    assert "<label for=\"entity\">Select an entity:</label>" in response.text
    assert "<input type=\"submit\" value=\"Show Statistics\">" in response.text

def test_get_stats_no_year_range():
    response = client.post("/get_stats/", data={"entity": "Albania"})
    assert response.status_code == 200
    assert "<p>Statistics for all parameters for Albania for all years:</p>" in response.text

def test_get_stats_valid_year_range():
    response = client.post("/get_stats/", data={"entity": "Albania", "start_year": 2000, "end_year": 2020})
    assert response.status_code == 200
    assert "Year range must be between 1750 and 2022" not in response.text  # Ensure no error message is present

def test_get_stats_invalid_year_range():
    response = client.post("/get_stats/", data={"entity": "Albania", "start_year": 1700, "end_year": 2025})
    assert response.status_code == 200
    assert "<p>Year range must be between 1750 and 2022</p>" in response.text

def test_get_stats_exception_handling():
    response = client.post("/get_stats/", data={"entity": "Albania", "start_year": "invalid", "end_year": "invalid"})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "start_year"],
                "msg": "Input should be a valid integer, unable to parse string as an integer",
                "type": "int_parsing",
                "input": "invalid"
            },
            {
                "loc": ["body", "end_year"],
                "msg": "Input should be a valid integer, unable to parse string as an integer",
                "type": "int_parsing",
                "input": "invalid"
            }
        ]
    }

