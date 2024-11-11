from typing import List
from pydantic import BaseModel


class PowerOutput(BaseModel):
    name: str
    p: float
