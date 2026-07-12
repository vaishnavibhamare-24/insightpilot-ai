from fastapi import APIRouter

from backend.schemas.data_quality import (
    DataQualityReportResponse,
)
from backend.services.data_quality_service import (
    DataQualityService,
)


router = APIRouter()

data_quality_service = DataQualityService()


@router.get(
    "/report",
    response_model=DataQualityReportResponse,
)
def get_data_quality_report():
    return data_quality_service.get_latest_report()