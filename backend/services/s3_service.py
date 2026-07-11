from __future__ import annotations

from botocore.exceptions import (
    BotoCoreError,
    ClientError,
    NoCredentialsError,
    ProfileNotFound,
)

from backend.config.settings import get_settings
from backend.services.aws_session import get_aws_session

settings = get_settings()


class S3Service:
    def __init__(self) -> None:
        if not settings.s3_raw_bucket:
            raise RuntimeError(
                "S3_RAW_BUCKET is not configured in the .env file."
            )

        try:
            session = get_aws_session()
            self.client = session.client("s3")
        except ProfileNotFound as exc:
            raise RuntimeError(
                f"AWS profile '{settings.aws_profile}' was not found."
            ) from exc

    def list_raw_objects(self) -> list[dict]:
        """
        Return every non-empty object stored in the raw S3 bucket.

        Pagination is used so the service continues working when the
        bucket contains more than 1,000 objects.
        """
        objects: list[dict] = []

        try:
            paginator = self.client.get_paginator("list_objects_v2")

            page_iterator = paginator.paginate(
                Bucket=settings.s3_raw_bucket,
            )

            for page in page_iterator:
                for item in page.get("Contents", []):
                    key = item["Key"]
                    size = int(item.get("Size", 0))

                    # Ignore zero-byte objects used only as folder markers.
                    if key.endswith("/") and size == 0:
                        continue

                    last_modified = item.get("LastModified")

                    objects.append(
                        {
                            "key": key,
                            "size_bytes": size,
                            "last_modified": (
                                last_modified.isoformat()
                                if last_modified
                                else None
                            ),
                            "storage_class": item.get(
                                "StorageClass"
                            ),
                        }
                    )

            return objects

        except NoCredentialsError as exc:
            raise RuntimeError(
                "AWS credentials were not found."
            ) from exc

        except ClientError as exc:
            error = exc.response.get("Error", {})
            error_code = error.get("Code", "Unknown")
            error_message = error.get(
                "Message",
                "Unable to access the S3 bucket.",
            )

            raise RuntimeError(
                f"S3 error {error_code}: {error_message}"
            ) from exc

        except BotoCoreError as exc:
            raise RuntimeError(
                "AWS SDK could not communicate with S3."
            ) from exc