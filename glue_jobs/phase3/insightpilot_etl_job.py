import sys

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import DecimalType


args = getResolvedOptions(
    sys.argv,
    [
        "JOB_NAME",
        "RAW_DATABASE",
        "PROCESSED_BUCKET",
    ],
)

sc = SparkContext()
glue_context = GlueContext(sc)
spark = glue_context.spark_session

job = Job(glue_context)
job.init(args["JOB_NAME"], args)

RAW_DATABASE = args["RAW_DATABASE"]
PROCESSED_BUCKET = args["PROCESSED_BUCKET"].rstrip("/")


def read_glue_table(table_name: str) -> DataFrame:
    """
    Read a table from the AWS Glue Data Catalog.
    """
    dynamic_frame = glue_context.create_dynamic_frame.from_catalog(
        database=RAW_DATABASE,
        table_name=table_name,
    )

    return dynamic_frame.toDF()


def normalize_column_names(df: DataFrame) -> DataFrame:
    """
    Convert column names to lowercase snake_case.
    """
    for old_column in df.columns:
        new_column = (
            old_column.strip()
            .lower()
            .replace(" ", "_")
            .replace("-", "_")
            .replace("/", "_")
        )

        df = df.withColumnRenamed(old_column, new_column)

    return df


def remove_duplicate_rows(
    df: DataFrame,
    key_columns: list[str],
) -> DataFrame:
    """
    Remove duplicate records using the provided business key.
    """
    existing_keys = [
        column
        for column in key_columns
        if column in df.columns
    ]

    if not existing_keys:
        return df.dropDuplicates()

    return df.dropDuplicates(existing_keys)


def trim_string_columns(df: DataFrame) -> DataFrame:
    """
    Remove leading and trailing spaces from string columns.
    """
    for field in df.schema.fields:
        if field.dataType.simpleString() == "string":
            df = df.withColumn(
                field.name,
                F.trim(F.col(field.name)),
            )

    return df


def write_parquet(
    df: DataFrame,
    output_name: str,
    partition_columns: list[str] | None = None,
) -> None:
    """
    Write a DataFrame to the processed S3 bucket in Parquet format.
    """
    output_path = f"{PROCESSED_BUCKET}/{output_name}/"

    writer = (
        df.write
        .mode("overwrite")
        .format("parquet")
    )

    if partition_columns:
        valid_partitions = [
            column
            for column in partition_columns
            if column in df.columns
        ]

        if valid_partitions:
            writer = writer.partitionBy(*valid_partitions)

    writer.save(output_path)


customers_raw = read_glue_table("customers")
products_raw = read_glue_table("products")
orders_raw = read_glue_table("orders")
payments_raw = read_glue_table("payments")
refunds_raw = read_glue_table("refunds")
support_tickets_raw = read_glue_table("support_tickets")


customers_raw = normalize_column_names(customers_raw)
products_raw = normalize_column_names(products_raw)
orders_raw = normalize_column_names(orders_raw)
payments_raw = normalize_column_names(payments_raw)
refunds_raw = normalize_column_names(refunds_raw)
support_tickets_raw = normalize_column_names(support_tickets_raw)


customers_raw = trim_string_columns(customers_raw)
products_raw = trim_string_columns(products_raw)
orders_raw = trim_string_columns(orders_raw)
payments_raw = trim_string_columns(payments_raw)
refunds_raw = trim_string_columns(refunds_raw)
support_tickets_raw = trim_string_columns(support_tickets_raw)


# ---------------------------------------------------------
# Step 23.8 — Build dim_customers
# ---------------------------------------------------------

customers = remove_duplicate_rows(
    customers_raw,
    ["customer_id"],
)

customers = customers.filter(
    F.col("customer_id").isNotNull()
)

if "email" in customers.columns:
    customers = customers.withColumn(
        "email",
        F.lower(F.col("email")),
    )

if "first_name" in customers.columns:
    customers = customers.withColumn(
        "first_name",
        F.initcap(F.col("first_name")),
    )

if "last_name" in customers.columns:
    customers = customers.withColumn(
        "last_name",
        F.initcap(F.col("last_name")),
    )

if "city" in customers.columns:
    customers = customers.withColumn(
        "city",
        F.initcap(F.col("city")),
    )

if "state" in customers.columns:
    customers = customers.withColumn(
        "state",
        F.upper(F.col("state")),
    )

if "country" in customers.columns:
    customers = customers.withColumn(
        "country",
        F.upper(F.col("country")),
    )

if "signup_date" in customers.columns:
    customers = customers.withColumn(
        "signup_date",
        F.to_date(F.col("signup_date")),
    )

if "date_of_birth" in customers.columns:
    customers = customers.withColumn(
        "date_of_birth",
        F.to_date(F.col("date_of_birth")),
    )

if "customer_segment" in customers.columns:
    customers = customers.fillna(
        {
            "customer_segment": "Unknown",
        }
    )

dim_customers = customers.withColumn(
    "customer_created_timestamp",
    F.current_timestamp(),
)

write_parquet(
    dim_customers,
    "dim_customers",
)


# ---------------------------------------------------------
# Step 23.9 — Build dim_products
# ---------------------------------------------------------

products = remove_duplicate_rows(
    products_raw,
    ["product_id"],
)

products = products.filter(
    F.col("product_id").isNotNull()
)

if "product_name" in products.columns:
    products = products.withColumn(
        "product_name",
        F.initcap(F.col("product_name")),
    )

if "category" in products.columns:
    products = products.withColumn(
        "category",
        F.initcap(F.col("category")),
    )

if "subcategory" in products.columns:
    products = products.withColumn(
        "subcategory",
        F.initcap(F.col("subcategory")),
    )

if "brand" in products.columns:
    products = products.withColumn(
        "brand",
        F.initcap(F.col("brand")),
    )

if "price" in products.columns:
    products = products.withColumn(
        "price",
        F.col("price").cast(DecimalType(18, 2)),
    )

if "cost" in products.columns:
    products = products.withColumn(
        "cost",
        F.col("cost").cast(DecimalType(18, 2)),
    )

if "stock_quantity" in products.columns:
    products = products.withColumn(
        "stock_quantity",
        F.col("stock_quantity").cast("integer"),
    )

product_fill_values = {}

if "category" in products.columns:
    product_fill_values["category"] = "Unknown"

if "subcategory" in products.columns:
    product_fill_values["subcategory"] = "Unknown"

if "brand" in products.columns:
    product_fill_values["brand"] = "Unknown"

if "stock_quantity" in products.columns:
    product_fill_values["stock_quantity"] = 0

if product_fill_values:
    products = products.fillna(product_fill_values)

if "price" in products.columns:
    products = products.filter(
        F.col("price") >= 0
    )

dim_products = products.withColumn(
    "product_created_timestamp",
    F.current_timestamp(),
)

write_parquet(
    dim_products,
    "dim_products",
)

# ---------------------------------------------------------
# Step 23.10 — Build fact_orders
# ---------------------------------------------------------

orders = remove_duplicate_rows(
    orders_raw,
    ["order_id"],
)

orders = orders.filter(
    F.col("order_id").isNotNull()
)

orders = orders.filter(
    F.col("customer_id").isNotNull()
)

if "order_date" in orders.columns:
    orders = orders.withColumn(
        "order_date",
        F.to_timestamp(F.col("order_date")),
    )

    orders = orders.withColumn(
        "order_year",
        F.year(F.col("order_date")),
    )

    orders = orders.withColumn(
        "order_month",
        F.month(F.col("order_date")),
    )

    orders = orders.withColumn(
        "order_day",
        F.dayofmonth(F.col("order_date")),
    )

    orders = orders.withColumn(
        "order_date_only",
        F.to_date(F.col("order_date")),
    )

if "quantity" in orders.columns:
    orders = orders.withColumn(
        "quantity",
        F.col("quantity").cast("integer"),
    )

if "unit_price" in orders.columns:
    orders = orders.withColumn(
        "unit_price",
        F.col("unit_price").cast(DecimalType(18, 2)),
    )

if "discount" in orders.columns:
    orders = orders.withColumn(
        "discount",
        F.coalesce(
            F.col("discount").cast(DecimalType(18, 2)),
            F.lit(0).cast(DecimalType(18, 2)),
        ),
    )

if "total_amount" in orders.columns:
    orders = orders.withColumn(
        "total_amount",
        F.col("total_amount").cast(DecimalType(18, 2)),
    )

if (
    "total_amount" not in orders.columns
    and "quantity" in orders.columns
    and "unit_price" in orders.columns
):
    orders = orders.withColumn(
        "total_amount",
        (
            F.col("quantity") * F.col("unit_price")
        ).cast(DecimalType(18, 2)),
    )

if "quantity" in orders.columns:
    orders = orders.filter(
        F.col("quantity") > 0
    )

if "total_amount" in orders.columns:
    orders = orders.filter(
        F.col("total_amount") >= 0
    )

if "order_status" in orders.columns:
    orders = orders.withColumn(
        "order_status",
        F.upper(F.col("order_status")),
    )

fact_orders = orders.withColumn(
    "etl_loaded_timestamp",
    F.current_timestamp(),
)

write_parquet(
    fact_orders,
    "fact_orders",
    ["order_year", "order_month"],
)

# ---------------------------------------------------------
# Step 23.11 — Build fact_payments
# ---------------------------------------------------------

payments = remove_duplicate_rows(
    payments_raw,
    ["payment_id"],
)

payments = payments.filter(
    F.col("payment_id").isNotNull()
)

payments = payments.filter(
    F.col("order_id").isNotNull()
)

if "payment_date" in payments.columns:
    payments = payments.withColumn(
        "payment_date",
        F.to_timestamp(F.col("payment_date")),
    )

    payments = payments.withColumn(
        "payment_year",
        F.year(F.col("payment_date")),
    )

    payments = payments.withColumn(
        "payment_month",
        F.month(F.col("payment_date")),
    )

if "payment_amount" in payments.columns:
    payments = payments.withColumn(
        "payment_amount",
        F.col("payment_amount").cast(DecimalType(18, 2)),
    )

    payments = payments.filter(
        F.col("payment_amount") >= 0
    )

if "payment_method" in payments.columns:
    payments = payments.withColumn(
        "payment_method",
        F.upper(F.col("payment_method")),
    )

if "payment_status" in payments.columns:
    payments = payments.withColumn(
        "payment_status",
        F.upper(F.col("payment_status")),
    )

fact_payments = payments.withColumn(
    "etl_loaded_timestamp",
    F.current_timestamp(),
)

write_parquet(
    fact_payments,
    "fact_payments",
    ["payment_year", "payment_month"],
)


# ---------------------------------------------------------
# Step 23.12 — Build fact_refunds
# ---------------------------------------------------------

refunds = remove_duplicate_rows(
    refunds_raw,
    ["refund_id"],
)

refunds = refunds.filter(
    F.col("refund_id").isNotNull()
)

refunds = refunds.filter(
    F.col("order_id").isNotNull()
)

if "refund_date" in refunds.columns:
    refunds = refunds.withColumn(
        "refund_date",
        F.to_timestamp(F.col("refund_date")),
    )

    refunds = refunds.withColumn(
        "refund_year",
        F.year(F.col("refund_date")),
    )

    refunds = refunds.withColumn(
        "refund_month",
        F.month(F.col("refund_date")),
    )

if "refund_amount" in refunds.columns:
    refunds = refunds.withColumn(
        "refund_amount",
        F.col("refund_amount").cast(DecimalType(18, 2)),
    )

    refunds = refunds.filter(
        F.col("refund_amount") >= 0
    )

if "refund_status" in refunds.columns:
    refunds = refunds.withColumn(
        "refund_status",
        F.upper(F.col("refund_status")),
    )

if "refund_reason" in refunds.columns:
    refunds = refunds.fillna(
        {
            "refund_reason": "Unknown",
        }
    )

fact_refunds = refunds.withColumn(
    "etl_loaded_timestamp",
    F.current_timestamp(),
)

write_parquet(
    fact_refunds,
    "fact_refunds",
    ["refund_year", "refund_month"],
)

# ---------------------------------------------------------
# Step 23.13 — Build fact_support_tickets
# ---------------------------------------------------------

support_tickets = remove_duplicate_rows(
    support_tickets_raw,
    ["ticket_id"],
)

support_tickets = support_tickets.filter(
    F.col("ticket_id").isNotNull()
)

support_tickets = support_tickets.filter(
    F.col("customer_id").isNotNull()
)

if "created_date" in support_tickets.columns:
    support_tickets = support_tickets.withColumn(
        "created_date",
        F.to_timestamp(F.col("created_date")),
    )

    support_tickets = support_tickets.withColumn(
        "ticket_year",
        F.year(F.col("created_date")),
    )

    support_tickets = support_tickets.withColumn(
        "ticket_month",
        F.month(F.col("created_date")),
    )

if "resolved_date" in support_tickets.columns:
    support_tickets = support_tickets.withColumn(
        "resolved_date",
        F.to_timestamp(F.col("resolved_date")),
    )

if (
    "created_date" in support_tickets.columns
    and "resolved_date" in support_tickets.columns
):
    support_tickets = support_tickets.withColumn(
        "resolution_hours",
        (
            F.unix_timestamp(F.col("resolved_date"))
            - F.unix_timestamp(F.col("created_date"))
        ) / 3600,
    )

if "priority" in support_tickets.columns:
    support_tickets = support_tickets.withColumn(
        "priority",
        F.upper(F.col("priority")),
    )

if "status" in support_tickets.columns:
    support_tickets = support_tickets.withColumn(
        "status",
        F.upper(F.col("status")),
    )

if "category" in support_tickets.columns:
    support_tickets = support_tickets.fillna(
        {
            "category": "Unknown",
        }
    )

if "satisfaction_score" in support_tickets.columns:
    support_tickets = support_tickets.withColumn(
        "satisfaction_score",
        F.col("satisfaction_score").cast("double"),
    )

fact_support_tickets = support_tickets.withColumn(
    "etl_loaded_timestamp",
    F.current_timestamp(),
)

write_parquet(
    fact_support_tickets,
    "fact_support_tickets",
    ["ticket_year", "ticket_month"],
)

# ---------------------------------------------------------
# Step 23.14 — Create customer order and CLV features
# ---------------------------------------------------------

customer_order_features = (
    fact_orders
    .groupBy("customer_id")
    .agg(
        F.countDistinct("order_id").alias("total_orders"),
        F.sum("total_amount").alias("lifetime_revenue"),
        F.avg("total_amount").alias("average_order_value"),
        F.min("order_date").alias("first_order_date"),
        F.max("order_date").alias("last_order_date"),
    )
)

customer_order_features = customer_order_features.withColumn(
    "days_since_last_order",
    F.datediff(
        F.current_date(),
        F.to_date(F.col("last_order_date")),
    ),
)

customer_order_features = customer_order_features.withColumn(
    "customer_lifetime_days",
    F.datediff(
        F.to_date(F.col("last_order_date")),
        F.to_date(F.col("first_order_date")),
    ),
)

customer_order_features = customer_order_features.withColumn(
    "purchase_frequency",
    F.when(
        F.col("customer_lifetime_days") > 0,
        F.col("total_orders") / F.col("customer_lifetime_days"),
    ).otherwise(
        F.col("total_orders")
    ),
)

customer_order_features = customer_order_features.withColumn(
    "estimated_clv",
    (
        F.col("average_order_value")
        * F.col("total_orders")
    ).cast(DecimalType(18, 2)),
)

# ---------------------------------------------------------
# Step 23.15 — Create churn labels and customer_features
# ---------------------------------------------------------

customer_order_features = customer_order_features.withColumn(
    "churn_label",
    F.when(
        F.col("days_since_last_order") > 90,
        F.lit(1),
    ).otherwise(
        F.lit(0)
    ),
)

customer_features = (
    dim_customers
    .join(
        customer_order_features,
        on="customer_id",
        how="left",
    )
)

customer_feature_fill_values = {}

if "total_orders" in customer_features.columns:
    customer_feature_fill_values["total_orders"] = 0

if "lifetime_revenue" in customer_features.columns:
    customer_feature_fill_values["lifetime_revenue"] = 0

if "average_order_value" in customer_features.columns:
    customer_feature_fill_values["average_order_value"] = 0

if "days_since_last_order" in customer_features.columns:
    customer_feature_fill_values["days_since_last_order"] = 9999

if "customer_lifetime_days" in customer_features.columns:
    customer_feature_fill_values["customer_lifetime_days"] = 0

if "purchase_frequency" in customer_features.columns:
    customer_feature_fill_values["purchase_frequency"] = 0

if "estimated_clv" in customer_features.columns:
    customer_feature_fill_values["estimated_clv"] = 0

if "churn_label" in customer_features.columns:
    customer_feature_fill_values["churn_label"] = 1

if customer_feature_fill_values:
    customer_features = customer_features.fillna(
        customer_feature_fill_values
    )

write_parquet(
    customer_features,
    "customer_features",
)

# ---------------------------------------------------------
# Step 23.16 — Create monthly revenue features
# ---------------------------------------------------------

if "order_status" in fact_orders.columns:
    completed_orders = fact_orders.filter(
        ~F.col("order_status").isin(
            "CANCELLED",
            "CANCELED",
            "FAILED",
        )
    )
else:
    completed_orders = fact_orders

revenue_features = (
    completed_orders
    .filter(
        F.col("order_date").isNotNull()
    )
    .groupBy(
        "order_year",
        "order_month",
    )
    .agg(
        F.countDistinct("order_id").alias("monthly_orders"),
        F.countDistinct("customer_id").alias("monthly_customers"),
        F.sum("total_amount").alias("gross_revenue"),
        F.avg("total_amount").alias("average_order_value"),
        F.sum("quantity").alias("units_sold"),
    )
)

revenue_features = revenue_features.withColumn(
    "revenue_month",
    F.to_date(
        F.concat_ws(
            "-",
            F.col("order_year"),
            F.lpad(
                F.col("order_month").cast("string"),
                2,
                "0",
            ),
            F.lit("01"),
        )
    ),
)

write_parquet(
    revenue_features,
    "revenue_features",
    ["order_year"],
)


# ---------------------------------------------------------
# Step 23.17 — Create product performance features
# ---------------------------------------------------------

product_performance = (
    fact_orders
    .groupBy("product_id")
    .agg(
        F.countDistinct("order_id").alias("total_product_orders"),
        F.sum("quantity").alias("total_units_sold"),
        F.sum("total_amount").alias("product_revenue"),
        F.avg("unit_price").alias("average_selling_price"),
        F.countDistinct("customer_id").alias("unique_customers"),
    )
)

product_performance = (
    dim_products
    .join(
        product_performance,
        on="product_id",
        how="left",
    )
)

product_performance_fill_values = {}

if "total_product_orders" in product_performance.columns:
    product_performance_fill_values["total_product_orders"] = 0

if "total_units_sold" in product_performance.columns:
    product_performance_fill_values["total_units_sold"] = 0

if "product_revenue" in product_performance.columns:
    product_performance_fill_values["product_revenue"] = 0

if "average_selling_price" in product_performance.columns:
    product_performance_fill_values["average_selling_price"] = 0

if "unique_customers" in product_performance.columns:
    product_performance_fill_values["unique_customers"] = 0

if product_performance_fill_values:
    product_performance = product_performance.fillna(
        product_performance_fill_values
    )

if (
    "cost" in product_performance.columns
    and "total_units_sold" in product_performance.columns
):
    product_performance = product_performance.withColumn(
        "estimated_product_cost",
        (
            F.col("cost")
            * F.col("total_units_sold")
        ).cast(DecimalType(18, 2)),
    )

    product_performance = product_performance.withColumn(
        "estimated_profit",
        (
            F.col("product_revenue")
            - F.col("estimated_product_cost")
        ).cast(DecimalType(18, 2)),
    )

write_parquet(
    product_performance,
    "product_performance",
)

job.commit()