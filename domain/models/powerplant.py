from typing import List
from pydantic import BaseModel

from .fuel import Fuel


class Powerplant(BaseModel):
    name: str
    type: str
    efficiency: float
    pmin: float
    pmax: float
    cost: float = 0

    def calculate_cost(self, fuels: Fuel, include_co2: bool):
        """Calculates PowerPlant costs"""
        if self.type == "gasfired":
            self.cost = fuels.gas / self.efficiency
            if include_co2:
                self.cost += fuels.co2 * 0.3  # each mwh generates 0.3 tons of CO2
        elif self.type == "turbojet":
            self.cost = fuels.kerosine / self.efficiency
        elif self.type == "windturbine":
            self.cost = 0
