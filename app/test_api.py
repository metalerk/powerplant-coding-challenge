import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)

# Sample payload for a standard test case
standard_payload = {
    "load": 480,
    "fuels": {
        "gas": 13.4,
        "kerosine": 50.8,
        "co2": 20,
        "wind": 60
    },
    "powerplants": [
        {"name": "gasfiredbig1", "type": "gasfired", "efficiency": 0.53, "pmin": 100, "pmax": 460},
        {"name": "gasfiredbig2", "type": "gasfired", "efficiency": 0.53, "pmin": 100, "pmax": 460},
        {"name": "windpark1", "type": "windturbine", "efficiency": 1, "pmin": 0, "pmax": 150}
    ],
    "include_co2": True
}

def test_production_plan_endpoint_standard_case():
    """Test the /productionplan endpoint with a standard payload"""
    response = client.post("/productionplan", json=standard_payload)
    assert response.status_code == 200

    result = response.json()
    
    # Verify the total power output matches the load
    total_generated = sum(output["p"] for output in result)
    assert total_generated == pytest.approx(480, rel=1e-2)

    # Verify each power plant in the result has a valid power output
    for output in result:
        assert output["p"] >= 0


def test_production_plan_endpoint_zero_load():
    """Test with a load of zero to ensure the system returns zero power output for each plant"""
    payload = standard_payload.copy()
    payload["load"] = 0
    response = client.post("/productionplan", json=payload)
    assert response.status_code == 200

    result = response.json()
    
    # Verify all plants produce 0 power if load is zero
    for output in result:
        assert output["p"] == 0.0


def test_production_plan_endpoint_excessive_load():
    """Test with a load that exceeds the combined maximum capacity of all power plants"""
    payload = standard_payload.copy()
    payload["load"] = 2000  # Set a high load that cannot be met
    response = client.post("/productionplan", json=payload)
    
    # Check that the API returns an error for unmet load
    assert response.status_code == 400
    assert "Unable to meet the required energy load with given powerplants" == response.json()["detail"]


def test_production_plan_endpoint_missing_fuels():
    """Test with missing fuel data to ensure validation errors are correctly handled"""
    payload = standard_payload.copy()
    payload["fuels"].pop("gas")  # Remove 'gas' fuel type from payload
    response = client.post("/productionplan", json=payload)
    
    # Expect a 422 error for missing fields
    assert response.status_code == 422

