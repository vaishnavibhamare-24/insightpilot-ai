from pydantic import BaseModel


class HomeResponse(BaseModel):
    message: str
    status: str


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str