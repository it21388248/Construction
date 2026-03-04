from fastapi import APIRouter
from .schemas import SkimcoatPredictRequest, SkimcoatPredictResponse
from .service import predict_skimcoat, SCHEMA

router = APIRouter()

@router.get("/schema")
def get_schema():
    return SCHEMA or {"detail": "schema.json not found"}

@router.post("/predict", response_model=SkimcoatPredictResponse)
def predict(req: SkimcoatPredictRequest):
    brand, pps = predict_skimcoat(req)
    return SkimcoatPredictResponse(brand=brand, used_price_per_sqft_lkr=pps)