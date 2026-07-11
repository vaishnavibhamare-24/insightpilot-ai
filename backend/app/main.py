from fastapi import FastAPI

from backend.api.v1.router import api_router
from backend.schemas.common import HomeResponse


app = FastAPI(
    title="InsightPilot AI",
    description="Agentic Enterprise Data Intelligence Platform",
    version="1.0.0",
)

app.include_router(
    api_router,
    prefix="/api/v1",
)


@app.get(
    "/",
    tags=["Root"],
    response_model=HomeResponse,
)
def home() -> HomeResponse:
    return HomeResponse(
        message="Welcome to InsightPilot AI",
        status="Backend is running successfully!",
    )