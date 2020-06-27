import boto3
from botocore.exceptions import ClientError
import json
from src.errors import UnknownError


SANDMAN_TAG = "sandman"
IGNORE_TAG = "ignore"


def __is_ignorable(tags: list) -> bool:
    """
    Verifies if based on the tags, it should be ignored or not.
    If tags is None, it is not ignored.
    :param tags: a list with an instance's tags.
    :return: a boolean if it should be ignored or not.
    """
    if tags:
        for tag in tags:
            if tag["Key"] == SANDMAN_TAG and tag["Value"] == IGNORE_TAG:
                return True
    return False


def __retrieve_instances(client) -> list:
    """
    Retrieves a list of instance ids. All the instances with
    tag SANDMAN_TAG and value IGNORE_TAG will be excluded.
    :param client: boto3.client("ec2") object.
    :return: list of instance ids that are not ignored.
    """
    instances = client.describe_instances()
    instance_ids = []
    if instances:
        for reservation in instances["Reservations"]:
            for instance in reservation["Instances"]:
                if instance and not __is_ignorable(instance.get("Tags")):
                    instance_ids.append(instance["InstanceId"])
    return instance_ids


def start_instances() -> dict:
    """
    Starts the instances that are not ignored by SANDMAN_TAG=IGNORE_TAG.
    :return: a dictionary with the status code and a message.
    :raises UnknownError: if a ClientError occurs.
    """
    try:
        client = boto3.client("ec2")
        instances = __retrieve_instances(client)
        client.start_instances(InstanceIds=instances)
        return {
            "status_code": 200,
            "body": json.dumps(
                f"Started {len(instances)} instances " f"successfully"
            ),
        }
    except ClientError:
        raise UnknownError


def stop_instances():
    """
    Stops the instances that are not ignored by SANDMAN_TAG=IGNORE_TAG.
    :return: a dictionary with the status code and a message.
    :raises UnknownError: if a ClientError occurs.
    """
    try:
        client = boto3.client("ec2")
        instances = __retrieve_instances(client)
        client.stop_instances(InstanceIds=instances)
        return {
            "status_code": 200,
            "body": json.dumps(
                f"Stopped {len(instances)} instances " f"successfully"
            ),
        }
    except ClientError:
        raise UnknownError
