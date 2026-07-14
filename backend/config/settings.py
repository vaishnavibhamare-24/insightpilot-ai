from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bedrock_knowledge_base_id: str = ""
    bedrock_model_arn: str = ""
    bedrock_rag_number_of_results: int = 5

    app_name: str = "InsightPilot AI"
    app_version: str = "1.0.0"
    app_env: str = "development"

    aws_region: str = "us-east-1"
    aws_profile: str = "insightpilot"

    s3_raw_bucket: str = ""
    s3_processed_bucket: str = ""
    athena_output_bucket: str = ""

    glue_database: str = "insightpilot_raw_db"
    ml_artifacts_bucket: str = ""
    churn_model_s3_key: str = "models/churn/churn_model.joblib"
    forecast_model_s3_key: str = "models/forecast/revenue_model.joblib"
    mlflow_tracking_uri: str = (
    "sqlite:///ml/experiments/mlflow.db"
)
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
    sagemaker_role_arn: str = ""
    sagemaker_churn_endpoint_name: str = (
        "insightpilot-churn-endpoint"
    )
    sagemaker_model_name: str = (
        "insightpilot-churn-model"
    )
    sagemaker_endpoint_config_name: str = (
        "insightpilot-churn-endpoint-config"
    )
    sagemaker_instance_type: str = "ml.m5.large"
    sagemaker_capture_prefix: str = (
        "monitoring/churn/data-capture"
    )
    sagemaker_monitoring_prefix: str = (
        "monitoring/churn/reports"
    )



@lru_cache
def get_settings() -> Settings:
    return Settings()
