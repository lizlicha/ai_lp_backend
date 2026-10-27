"""Legacy Slack event entry point for the WordPress EC2 controller.

The deployed ``wordpress_main`` function uses this file as ``main.lambda_handler``.
Only a text message containing an explicit command invokes another Lambda.
"""

import json

import boto3


def _response(status, body):
    return {"statusCode": status, "body": body}


def lambda_handler(event, context):
    raw_body = event.get("body") if isinstance(event, dict) else None
    try:
        body = json.loads(raw_body) if isinstance(raw_body, str) else raw_body
    except json.JSONDecodeError:
        return _response(400, "invalid JSON")
    if not isinstance(body, dict):
        return _response(400, "invalid body")

    # Slack's URL verification has no event.text.
    if body.get("type") == "url_verification":
        challenge = body.get("challenge")
        return _response(200, challenge) if isinstance(challenge, str) else _response(400, "invalid challenge")

    slack_event = body.get("event")
    if not isinstance(slack_event, dict) or slack_event.get("type") != "message":
        return _response(200, "ignored")
    text = slack_event.get("text")
    if not isinstance(text, str) or not text.strip():
        return _response(200, "ignored")

    function_name = None
    if "起動" in text:
        function_name = "wordpress_start_ec2"
    if "停止" in text:
        function_name = "wordpress_end_ec2"
    if function_name:
        boto3.client("lambda").invoke(
            FunctionName=function_name,
            InvocationType="Event",
        )
    return _response(200, "ok")
