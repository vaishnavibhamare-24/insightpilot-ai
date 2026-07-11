from boto3.session import Session

from backend.config.settings import get_settings

settings = get_settings()


def get_aws_session() -> Session:
    return Session(
        profile_name=settings.aws_profile,
        region_name=settings.aws_region,
    )