from fastapi import APIRouter, HTTPException, status

from backend.config.settings import get_settings
from backend.schemas.storage import (
    S3Object,
    S3ObjectsResponse,
)
from backend.services.s3_service import S3Service

router = APIRouter()
settings = get_settings()


@router.get(
    "/raw",
    response_model=S3ObjectsResponse,
    summary="List raw S3 objects",
    description=(
        "Lists files currently stored in the InsightPilot raw S3 bucket."
    ),
)
def list_raw_storage() -> S3ObjectsResponse:
    try:
        objects = S3Service().list_raw_objects()

        return S3ObjectsResponse(
            bucket=settings.s3_raw_bucket,
            object_count=len(objects),
            total_size_bytes=sum(
                item["size_bytes"] for item in objects
            ),
            objects=[
                S3Object(**item)
                for item in objects
            ],
        )

    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc