from fastapi import FastAPI
from api_service.app.api.v1.endpoints import upload, status
from shared.database import engine, Base
import logging

# Create tables (Auto-create for simplicity)
Base.metadata.create_all(bind=engine)

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="AI Doc Processor API")

app.include_router(upload.router, prefix="/api/v1/documents", tags=["Upload"])
app.include_router(status.router, prefix="/api/v1/documents", tags=["Status"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
