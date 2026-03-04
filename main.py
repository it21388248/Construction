
from fastapi import FastAPI
from app.health import router as health_router
from app.paint.router import router as paint_router
from app.skimcoat.router import router as skimcoat_router

app = FastAPI(title="Construction Material Predictor API")

app.include_router(health_router)
app.include_router(paint_router, prefix="/paint", tags=["Paint"])
app.include_router(skimcoat_router, prefix="/skimcoat", tags=["Skimcoat"])