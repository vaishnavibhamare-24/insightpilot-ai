from pathlib import Path

from data_pipeline.data_generator.customers import generate_customers
from data_pipeline.data_generator.orders import generate_orders
from data_pipeline.data_generator.payments import generate_payments
from data_pipeline.data_generator.products import generate_products
from data_pipeline.data_generator.refunds import generate_refunds
from data_pipeline.data_generator.support_tickets import (
    generate_support_tickets,
)
from data_pipeline.data_generator.website_events import (
    generate_website_events,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "data_pipeline" / "raw_data"


def main() -> None:
    print("=" * 60)
    print("Generating InsightPilot e-commerce datasets")
    print("=" * 60)

    customers_df = generate_customers(
        OUTPUT_DIR / "customers.csv"
    )

    products_df = generate_products(
        OUTPUT_DIR / "products.csv"
    )

    orders_df = generate_orders(
        customers_df=customers_df,
        products_df=products_df,
        output_path=OUTPUT_DIR / "orders.csv",
    )

    payments_df = generate_payments(
        orders_df=orders_df,
        output_path=OUTPUT_DIR / "payments.csv",
    )

    refunds_df = generate_refunds(
        orders_df=orders_df,
        output_path=OUTPUT_DIR / "refunds.csv",
    )

    support_tickets_df = generate_support_tickets(
        customers_df=customers_df,
        orders_df=orders_df,
        output_path=OUTPUT_DIR / "support_tickets.csv",
    )

    website_events_df = generate_website_events(
        customers_df=customers_df,
        products_df=products_df,
        output_path=OUTPUT_DIR / "website_events.csv",
    )

    print("\nGeneration summary")
    print("-" * 60)
    print(f"Customers:       {len(customers_df):,}")
    print(f"Products:        {len(products_df):,}")
    print(f"Orders:          {len(orders_df):,}")
    print(f"Payments:        {len(payments_df):,}")
    print(f"Refunds:         {len(refunds_df):,}")
    print(f"Support tickets: {len(support_tickets_df):,}")
    print(f"Website events:  {len(website_events_df):,}")
    print("-" * 60)
    print(f"Output directory: {OUTPUT_DIR}")
    print("Dataset generation completed successfully.")


if __name__ == "__main__":
    main()