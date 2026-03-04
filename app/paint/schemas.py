from pydantic import BaseModel, Field
from typing import Optional, Literal

LocationT = Literal["indoor", "outdoor", "wood", "floor"]
SurfaceT = Literal["plaster", "concrete", "wood", "metal"]
FinishT = Literal["matte", "satin", "gloss"]
MoistureT = Literal["low", "medium", "high"]
PaintTypeT = Literal["emulsion", "enamel", "antifungal", "weatherproof"]

class PaintPredictRequest(BaseModel):
    wall_size_sqft: float = Field(..., gt=0)

    budget_lkr: Optional[float] = Field(None, gt=0)
    price_per_sqft_lkr: Optional[float] = Field(None, gt=0)

    location: LocationT
    surface_material: SurfaceT
    finish_type: FinishT
    coats_needed: int = Field(..., ge=1, le=3)
    moisture_level: MoistureT
    paint_type: PaintTypeT


class PaintPredictResponse(BaseModel):
    paint_brand: str
    paint_grade: str
    used_price_per_sqft_lkr: float