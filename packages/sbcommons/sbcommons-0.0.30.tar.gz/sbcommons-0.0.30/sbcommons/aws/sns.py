from typing import Any

import boto3


def sns_client() -> Any:
    return boto3.client('sns')


def publish(topic_arn: str, message: str):
    client = sns_client()
    client.publish(
        TargetArn=topic_arn,
        Message=message
    )
