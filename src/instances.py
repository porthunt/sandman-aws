import boto3
from botocore.exceptions import ClientError
from typing import Callable
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
            if (
                tag["Key"].lower() == SANDMAN_TAG
                and tag["Value"].lower() == IGNORE_TAG
            ):
                return True
    return False


def __get_tags(client, arn: str) -> list:
    tags = client.list_tags(ResourceArn=arn)
    if tags:
        return tags["Tags"]


def __interact_instances(client, action: Callable, status: str) -> dict:
    """
    Interacts with the instances. It executes the callable from action.
    :param client: Sagemaker boto3 client.
    :param action: a callable (e.g. client.start_notebook_instance).
    :param status: A status that will be verified before starting. If the
        status of the instance is not this one, it will not be executed.
    :return: A dictionary containing the status code and a body. Body shows
        the amount of affected instances.
    :raises UnknownError: if a ClientError occurs.
    """
    try:
        instances = client.list_notebook_instances()
        interaction = 0
        for instance in instances["NotebookInstances"]:
            tags = __get_tags(client, instance["NotebookInstanceArn"])
            if instance[
                "NotebookInstanceStatus"
            ] == status and not __is_ignorable(tags):
                interaction += 1
                action(NotebookInstanceName=instance["NotebookInstanceName"])
        return {
            "status_code": 200,
            "body": json.dumps(f"{interaction} instances affected"),
        }
    except ClientError:
        raise UnknownError


def start_instances() -> dict:
    """
    Starts the instances that are not ignored by SANDMAN_TAG=IGNORE_TAG.
    :return: a dictionary with the status code and a message.
    """
    client = boto3.client("sagemaker")
    action = client.start_notebook_instance
    return __interact_instances(client, action, "Stopped")


def stop_instances() -> dict:
    """
    Stops the instances that are not ignored by SANDMAN_TAG=IGNORE_TAG.
    :return: a dictionary with the status code and a message.
    """
    client = boto3.client("sagemaker")
    action = client.stop_notebook_instance
    return __interact_instances(client, action, "InService")
