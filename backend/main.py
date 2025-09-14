from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .app.api.v1.endpoints import fantasy
from .app.api.routers import waiver_router
from .app.core.config import settings

app = FastAPI(
    title="Yahoo Fantasy Football Analyst API",
    version="0.1.0",
    description="The backend API for the FFA project.",
)

# Include API routers
app.include_router(fantasy.router, prefix=settings.API_V1_STR, tags=["fantasy"])
app.include_router(waiver_router.router, prefix=settings.API_V1_STR, tags=["waiver"])

# Mount the static files (built React app)
# This allows FastAPI to serve the frontend in a production-like setup.
# In development, the Vite dev server (localhost:5173) is used.
app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.get("/api/health")
def health_check():
    """
    Simple health check endpoint.
    """
    return {"status": "ok"}
