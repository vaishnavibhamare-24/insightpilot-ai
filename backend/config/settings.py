from functools import lru_cache

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    # Application settings
    app_name: str = "InsightPilot AI"
    app_version: str = "1.0.0"
    app_env: str = "development"

    # AWS settings
    aws_region: str = "us-east-1"
    aws_profile: str = "insightpilot"

    # S3 settings
    s3_raw_bucket: str = ""
    s3_processed_bucket: str = ""
    athena_output_bucket: str = ""

    # AWS Glue settings
    glue_database: str = "insightpilot_raw_db"

    # Amazon Bedrock RAG settings
    bedrock_knowledge_base_id: str = ""
    bedrock_model_arn: str = ""
    bedrock_rag_number_of_results: int = 5

    # Phase 8 - Multi-Agent AI settings
    bedrock_chat_model_id: str = ""
    agent_max_steps: int = 8
    agent_default_timeout_seconds: int = 60
    agent_enable_llm_router: bool = False

    # Machine learning settings
    ml_artifacts_bucket: str = ""
    churn_model_s3_key: str = (
        "models/churn/churn_model.joblib"
    )
    forecast_model_s3_key: str = (
        "models/forecast/revenue_model.joblib"
    )

    # MLflow settings
    mlflow_tracking_uri: str = (
        "sqlite:///ml/experiments/mlflow.db"
    )

    # SageMaker settings
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

    # Pydantic settings configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()

