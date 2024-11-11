from typing import List

from fastapi import FastAPI, HTTPException

from domain.services import ProductionPlanService
from domain.models import PowerOutput
from .schemas import Payload


app = FastAPI()

@app.post("/productionplan", response_model=List[PowerOutput])
async def production_plan(payload: Payload):
    try:
        service = ProductionPlanService(
            load=payload.load,
            fuels=payload.fuels,
            powerplants=payload.powerplants,
            include_co2=payload.include_co2
        )
        result = service.generate_plan()
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
