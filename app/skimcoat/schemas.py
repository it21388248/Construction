from pydantic import BaseModel, Field
from typing import Optional, Literal

LocationT = Literal["indoor", "outdoor"]
SurfaceT = Literal["concrete", "cement-plaster", "plaster", "gypsum-board"]
MoistureT = Literal["low", "medium", "high"]
ConditionT = Literal["new", "old", "cracked"]
FinishT = Literal["basic", "smooth", "premium-smooth"]

class SkimcoatPredictRequest(BaseModel):
    wall_size_sqft: float = Field(..., gt=0)

    budget_lkr: Optional[float] = Field(None, gt=0)
    price_per_sqft_lkr: Optional[float] = Field(None, gt=0)

    location: LocationT
    surface_material: SurfaceT
    moisture_level: MoistureT
    substrate_condition: ConditionT
    coats_needed: int = Field(..., ge=1, le=3)
    finish_level: FinishT

class SkimcoatPredictResponse(BaseModel):
    brand: str
    used_price_per_sqft_lkr: float