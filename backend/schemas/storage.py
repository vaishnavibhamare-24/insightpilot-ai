from pydantic import BaseModel, Field


class S3Object(BaseModel):
    key: str
    size_bytes: int = Field(ge=0)
    last_modified: str | None = None
    storage_class: str | None = None


class S3ObjectsResponse(BaseModel):
    bucket: str
    object_count: int = Field(ge=0)
    total_size_bytes: int = Field(ge=0)
    objects: list[S3Object]