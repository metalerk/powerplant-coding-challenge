import pytest

from domain.services import ProductionPlanService
from domain.models import Powerplant, Fuel


# Sample fuel configuration for testing
fuels = Fuel(gas=13.4, kerosine=50.8, co2=20, wind=60)

# Sample list of power plants for testing
powerplants = [
    Powerplant(name="gasfiredbig1", type="gasfired", efficiency=0.53, pmin=100, pmax=460),
    Powerplant(name="gasfiredbig2", type="gasfired", efficiency=0.53, pmin=100, pmax=460),
    Powerplant(name="windpark1", type="windturbine", efficiency=1, pmin=0, pmax=150),
]

def test_production_plan_service_generates_correct_output():
    """Test that the production plan meets the specified load with correct power distribution."""
    # Initialize the service with a load that can be met by the available plants
    service = ProductionPlanService(load=480, fuels=fuels, powerplants=powerplants)
    result = service.generate_plan()
    total_generated = sum(output.p for output in result)
    # Verify that the total generated power matches the requested load within a small tolerance
    # Sets a relative tolerance of 1e-2, which is 0.01 or 1%
    assert total_generated == pytest.approx(480, rel=1e-2)

def test_production_plan_service_with_excessive_load():
    # Initialize the service with a load that can not be met by the available plants
    service = ProductionPlanService(load=2000, fuels=fuels, powerplants=powerplants)
    # assert it raises the expect exception
    with pytest.raises(ValueError, match="Unable to meet the required energy load with given powerplants"):
        service.generate_plan()
