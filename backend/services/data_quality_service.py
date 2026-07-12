import json

import boto3

from backend.config.settings import get_settings


class DataQualityService:
    def __init__(self):
        self.settings = get_settings()

        session = boto3.Session(
            profile_name=self.settings.aws_profile,
            region_name=self.settings.aws_region,
        )

        self.s3_client = session.client("s3")

    def get_latest_report(self) -> dict:
        bucket_name = (
            self.settings.s3_processed_bucket
            .replace("s3://", "")
            .rstrip("/")
        )

        response = self.s3_client.get_object(
            Bucket=bucket_name,
            Key="quality_reports/latest_report.json",
        )

        report_body = response["Body"].read()

        return json.loads(
            report_body.decode("utf-8")
        )