from typing import List, Optional
from pydantic import BaseModel

from domain.models import Fuel, Powerplant


class Payload(BaseModel):
    load: float
    fuels: Fuel
    powerplants: List[Powerplant]
    include_co2: Optional[bool] = False  # optional parameter for CO2 calculation
