import sys
import json
from datetime import datetime, timezone

import boto3

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql import functions as F


args = getResolvedOptions(
    sys.argv,
    [
        "JOB_NAME",
        "PROCESSED_DATABASE",
        "PROCESSED_BUCKET",
        "SNS_TOPIC_ARN",
    ],
)

sc = SparkContext()
glue_context = GlueContext(sc)
spark = glue_context.spark_session

job = Job(glue_context)
job.init(args["JOB_NAME"], args)

PROCESSED_DATABASE = args["PROCESSED_DATABASE"]
PROCESSED_BUCKET = args["PROCESSED_BUCKET"].rstrip("/")
SNS_TOPIC_ARN = args["SNS_TOPIC_ARN"]

s3_client = boto3.client("s3")
cloudwatch_client = boto3.client("cloudwatch")
sns_client = boto3.client("sns")


def read_table(table_name):
    return (
        glue_context
        .create_dynamic_frame
        .from_catalog(
            database=PROCESSED_DATABASE,
            table_name=table_name,
        )
        .toDF()
    )


def write_failed_records(df, rule_name):
    output_path = (
        f"{PROCESSED_BUCKET}/failed_records/"
        f"{rule_name}/"
    )

    df.write.mode("overwrite").parquet(output_path)


def create_rule_result(
    table_name,
    rule_name,
    passed,
    failed_records,
):
    return {
        "table_name": table_name,
        "rule_name": rule_name,
        "passed": passed,
        "failed_records": failed_records,
    }


quality_results = []

failed_customer_ids = dim_customers.filter(
    F.col("customer_id").isNull()
)

failed_count = failed_customer_ids.count()

quality_results.append(
    create_rule_result(
        "dim_customers",
        "customer_id_not_null",
        failed_count == 0,
        failed_count,
    )
)

if failed_count > 0:
    write_failed_records(
        failed_customer_ids,
        "customer_id_not_null",
    )

duplicate_customer_ids = (
    dim_customers
    .groupBy("customer_id")
    .count()
    .filter(F.col("count") > 1)
)

failed_count = duplicate_customer_ids.count()

quality_results.append(
    create_rule_result(
        "dim_customers",
        "customer_id_unique",
        failed_count == 0,
        failed_count,
    )
)

if failed_count > 0:
    write_failed_records(
        duplicate_customer_ids,
        "customer_id_unique",
    )

EMAIL_PATTERN = (
    r"^[A-Za-z0-9._%+-]+@"
    r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)

invalid_emails = dim_customers.filter(
    F.col("email").isNotNull()
    & ~F.col("email").rlike(EMAIL_PATTERN)
)

failed_count = invalid_emails.count()

quality_results.append(
    create_rule_result(
        "dim_customers",
        "email_format_valid",
        failed_count == 0,
        failed_count,
    )
)

if failed_count > 0:
    write_failed_records(
        invalid_emails,
        "email_format_valid",
    )

invalid_order_ids = fact_orders.filter(
    F.col("order_id").isNull()
)

failed_count = invalid_order_ids.count()

quality_results.append(
    create_rule_result(
        "fact_orders",
        "order_id_not_null",
        failed_count == 0,
        failed_count,
    )
)

if failed_count > 0:
    write_failed_records(
        invalid_order_ids,
        "order_id_not_null",
    )


duplicate_orders = (
    fact_orders
    .groupBy("order_id")
    .count()
    .filter(F.col("count") > 1)
)

failed_count = duplicate_orders.count()

quality_results.append(
    create_rule_result(
        "fact_orders",
        "order_id_unique",
        failed_count == 0,
        failed_count,
    )
)

if failed_count > 0:
    write_failed_records(
        duplicate_orders,
        "order_id_unique",
    )
future_orders = fact_orders.filter(
    F.to_date(F.col("order_date"))
    > F.current_date()
)

failed_count = future_orders.count()

quality_results.append(
    create_rule_result(
        "fact_orders",
        "order_date_not_future",
        failed_count == 0,
        failed_count,
    )
)

if failed_count > 0:
    write_failed_records(
        future_orders,
        "order_date_not_future",
    )

invalid_churn_labels = customer_features.filter(
    ~F.col("churn_label").isin(0, 1)
    | F.col("churn_label").isNull()
)

failed_count = invalid_churn_labels.count()

quality_results.append(
    create_rule_result(
        "customer_features",
        "churn_label_valid",
        failed_count == 0,
        failed_count,
    )
)

if failed_count > 0:
    write_failed_records(
        invalid_churn_labels,
        "churn_label_valid",
    )
invalid_clv = customer_features.filter(
    F.col("estimated_clv") < 0
)

failed_count = invalid_clv.count()

quality_results.append(
    create_rule_result(
        "customer_features",
        "clv_non_negative",
        failed_count == 0,
        failed_count,
    )
)

if failed_count > 0:
    write_failed_records(
        invalid_clv,
        "clv_non_negative",
    )
total_rules = len(quality_results)

passed_rules = sum(
    1
    for result in quality_results
    if result["passed"]
)

failed_rules = total_rules - passed_rules

quality_score = round(
    (passed_rules / total_rules) * 100,
    2,
) if total_rules else 0.0

total_failed_records = sum(
    result["failed_records"]
    for result in quality_results
)
if quality_score >= 95:
    quality_status = "HEALTHY"
elif quality_score >= 80:
    quality_status = "WARNING"
else:
    quality_status = "CRITICAL"
quality_report = {
    "generated_at": datetime.now(
        timezone.utc
    ).isoformat(),
    "overall_score": quality_score,
    "status": quality_status,
    "total_rules": total_rules,
    "passed_rules": passed_rules,
    "failed_rules": failed_rules,
    "failed_records": total_failed_records,
    "rules": quality_results,
}

bucket_name = PROCESSED_BUCKET.replace(
    "s3://",
    "",
)

report_body = json.dumps(
    quality_report,
    indent=2,
)

s3_client.put_object(
    Bucket=bucket_name,
    Key="quality_reports/latest_report.json",
    Body=report_body.encode("utf-8"),
    ContentType="application/json",
)
bucket_name = PROCESSED_BUCKET.replace(
    "s3://",
    "",
)

report_body = json.dumps(
    quality_report,
    indent=2,
)

s3_client.put_object(
    Bucket=bucket_name,
    Key="quality_reports/latest_report.json",
    Body=report_body.encode("utf-8"),
    ContentType="application/json",
)
cloudwatch_client.put_metric_data(
    Namespace="InsightPilot/DataQuality",
    MetricData=[
        {
            "MetricName": "QualityScore",
            "Value": quality_score,
            "Unit": "Percent",
        },
        {
            "MetricName": "FailedRules",
            "Value": failed_rules,
            "Unit": "Count",
        },
        {
            "MetricName": "FailedRecords",
            "Value": total_failed_records,
            "Unit": "Count",
        },
    ],
)
if quality_status in {"WARNING", "CRITICAL"}:
    sns_client.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject=(
            f"InsightPilot Data Quality "
            f"{quality_status}"
        ),
        Message=json.dumps(
            quality_report,
            indent=2,
        ),
    )
print(
    json.dumps(
        quality_report,
        indent=2,
    )
)

job.commit()
