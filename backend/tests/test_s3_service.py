from backend.services.s3_service import S3Service


def test_list_raw_objects() -> None:
    objects = S3Service().list_raw_objects()

    assert isinstance(objects, list)
    assert len(objects) >= 7

    keys = {
        item["key"]
        for item in objects
    }

    expected_keys = {
        "customers/customers.csv",
        "products/products.csv",
        "orders/orders.csv",
        "payments/payments.csv",
        "refunds/refunds.csv",
        "support_tickets/support_tickets.csv",
        "website_events/website_events.csv",
    }

    assert expected_keys.issubset(keys)