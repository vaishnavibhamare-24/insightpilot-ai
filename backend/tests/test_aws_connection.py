from backend.services.aws_session import get_aws_session


def test_aws_identity() -> None:
    session = get_aws_session()
    sts_client = session.client("sts")

    identity = sts_client.get_caller_identity()

    assert "Arn" in identity
    assert "Account" in identity

    print("AWS connection successful")