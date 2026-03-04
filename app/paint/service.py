import os
import json
import joblib
import pandas as pd
from fastapi import HTTPException

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ART_DIR = os.path.join(BASE_DIR, "artifacts")

MODEL_PATH = os.path.join(ART_DIR, "paint_recommender_enriched.joblib")
SCHEMA_PATH = os.path.join(ART_DIR, "schema.json")

# -----------------------------
# Load model once at startup
# -----------------------------
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Missing model file: {MODEL_PATH}")

MODEL = joblib.load(MODEL_PATH)

SCHEMA = {}
if os.path.exists(SCHEMA_PATH):
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        SCHEMA = json.load(f)


# -----------------------------
# Helper functions
# -----------------------------
def get_price_per_sqft(wall_size_sqft, budget_lkr, price_per_sqft_lkr):
    if price_per_sqft_lkr is not None:
        return float(price_per_sqft_lkr)

    if budget_lkr is None:
        raise HTTPException(
            status_code=400,
            detail="Provide either budget_lkr or price_per_sqft_lkr"
        )

    return float(budget_lkr) / float(wall_size_sqft)


def build_input_dataframe(req, price_per_sqft):
    return pd.DataFrame([{
        "WallSize_sqft": float(req.wall_size_sqft),
        "PricePerSqft_LKR": float(price_per_sqft),
        "CoatsNeeded": int(req.coats_needed),
        "Location": req.location.strip().lower(),
        "SurfaceMaterial": req.surface_material.strip().lower(),
        "FinishType": req.finish_type.strip().lower(),
        "MoistureLevel": req.moisture_level.strip().lower(),
        "PaintType": req.paint_type.strip().lower(),
    }])


def predict_paint(req):
    price_per_sqft = get_price_per_sqft(
        req.wall_size_sqft,
        req.budget_lkr,
        req.price_per_sqft_lkr
    )

    X = build_input_dataframe(req, price_per_sqft)
    prediction = MODEL.predict(X)

    return (
        str(prediction[0][0]),  # brand
        str(prediction[0][1]),  # grade
        float(price_per_sqft)
    )