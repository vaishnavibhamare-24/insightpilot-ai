from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "InsightPilot AI"
    app_version: str = "1.0.0"
    app_env: str = "development"

    aws_region: str = "us-east-1"
    aws_profile: str = "insightpilot"

    s3_raw_bucket: str = ""
    s3_processed_bucket: str = ""
    athena_output_bucket: str = ""

    glue_database: str = "insightpilot_db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings():
    return Settings()