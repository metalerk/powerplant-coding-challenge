from typing import List
from pydantic import BaseModel

class Fuel(BaseModel):
    gas: float
    kerosine: float
    co2: float
    wind: float
