import pytest
from fastapi.testclient import TestClient

import app.main as main

client = TestClient(main.app)  # Create a TestClient instance


# Define a list of dictionaries for different test cases
test_cases = [
    {"path": "/", "expected_status": 200, "expected_text": "Welcome to Air Pollution Data Viewer"},
    {
        "path": "/data/Germany/1750/2020/stats",
        "expected_status": 200,
        "expected_text": """    <p>Statistics for all parameters for Germany from 1750 to 2020:</p>

        <h3>Nitrogen Oxide (NOx)</h3>
        <ul>
            <li>Mean: 835946.1614044248</li>
            <li>Median: 671570.345</li>
            <li>Standard Deviation: 852202.1476415253</li>
        </ul> """,
    },
]


@pytest.mark.parametrize("test_data", test_cases)
def test_read_main(test_data):
    response = client.get(test_data["path"])  # Assuming there's a root endpoint
    assert response.status_code == test_data["expected_status"]
    assert test_data["expected_text"] in response.text
