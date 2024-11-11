from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)

payload = {
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
    ]
}

def test_production_plan_endpoint():
    response = client.post("/productionplan", json=payload)
    assert response.status_code == 200
    result = response.json()
    total_generated = sum(output["p"] for output in result)
    assert total_generated == pytest.approx(480, rel=1e-2)
