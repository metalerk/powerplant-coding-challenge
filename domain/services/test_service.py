import pytest

from domain.services import ProductionPlanService
from domain.models import Powerplant, Fuel


fuels = Fuel(gas=13.4, kerosine=50.8, co2=20, wind=60)

powerplants = [
    Powerplant(name="gasfiredbig1", type="gasfired", efficiency=0.53, pmin=100, pmax=460),
    Powerplant(name="gasfiredbig2", type="gasfired", efficiency=0.53, pmin=100, pmax=460),
    Powerplant(name="windpark1", type="windturbine", efficiency=1, pmin=0, pmax=150),
]

def test_production_plan_service_generates_correct_output():
    service = ProductionPlanService(load=480, fuels=fuels, powerplants=powerplants)
    result = service.generate_plan()
    total_generated = sum(output.p for output in result)
    assert total_generated == pytest.approx(480, rel=1e-2)

def test_production_plan_service_with_excessive_load():
    service = ProductionPlanService(load=2000, fuels=fuels, powerplants=powerplants)
    with pytest.raises(ValueError, match="Unable to meet the required load"):
        service.generate_plan()
