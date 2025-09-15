from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.endpoints import auth, yahoo
from app.core.config import settings
from app.core.db import Base, engine

# Create DB tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fantasy Sports API")

# CORS Middleware Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(auth.router, prefix=settings.API_V1_STR + "/auth", tags=["Authentication"])
app.include_router(yahoo.router, prefix=settings.API_V1_STR, tags=["Yahoo Integration"])

@app.get("/api/health")
def health_check():
    return {"status": "ok"}