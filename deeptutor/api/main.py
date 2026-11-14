"""DeepTutor FastAPI application entry point."""

from fastapi import FastAPI

from deeptutor.api.routers import router as api_router

app = FastAPI(
    title="DeepTutor API",
    description="Lifelong Personalized Tutoring — AI/ML developer tools",
    version="0.1.0",
)

app.include_router(api_router, prefix="/api")


@app.get("/health", include_in_schema=False)
async def health():
    """Health check endpoint."""
    return {"status": "ok", "version": "0.1.0"}


@app.get("/", include_in_schema=False)
async def root():
    """API root, returns available endpoints."""
    return {
        "name": "DeepTutor API",
        "version": "0.1.0",
        "endpoints": {
            "health": "/health",
            "courses": "/api/courses",
        }
    }
