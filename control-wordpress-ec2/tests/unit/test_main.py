import importlib.util
import json
from pathlib import Path
from unittest.mock import patch


SOURCE = Path(__file__).parents[2] / "src" / "main.py"
spec = importlib.util.spec_from_file_location("wordpress_main", SOURCE)
main = importlib.util.module_from_spec(spec)
spec.loader.exec_module(main)


def test_message_without_text_is_ignored():
    with patch.object(main.boto3, "client") as client:
        result = main.lambda_handler(
            {"body": json.dumps({"event": {"type": "message", "subtype": "message_deleted"}})},
            None,
        )
    assert result == {"statusCode": 200, "body": "ignored"}
    client.assert_not_called()


def test_text_command_invokes_once():
    with patch.object(main.boto3, "client") as client:
        result = main.lambda_handler(
            {"body": json.dumps({"event": {"type": "message", "text": "起動"}})},
            None,
        )
    assert result["statusCode"] == 200
    client.return_value.invoke.assert_called_once_with(
        FunctionName="wordpress_start_ec2", InvocationType="Event"
    )


def test_url_verification_without_event_text():
    with patch.object(main.boto3, "client") as client:
        result = main.lambda_handler(
            {"body": json.dumps({"type": "url_verification", "challenge": "test-challenge"})},
            None,
        )
    assert result == {"statusCode": 200, "body": "test-challenge"}
    client.assert_not_called()
