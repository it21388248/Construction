from fastapi import APIRouter
from .schemas import PaintPredictRequest, PaintPredictResponse
from .service import predict_paint, SCHEMA

router = APIRouter()

@router.get("/schema")
def get_schema():
    return SCHEMA or {"detail": "schema.json not found"}

@router.post("/predict", response_model=PaintPredictResponse)
def predict(req: PaintPredictRequest):
    brand, grade, pps = predict_paint(req)

    return PaintPredictResponse(
        paint_brand=brand,
        paint_grade=grade,
        used_price_per_sqft_lkr=pps
    )