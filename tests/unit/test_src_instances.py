import pytest
import boto3
from moto import mock_ec2
from src import instances


@pytest.fixture
def client():
    return boto3.client("ec2", region_name="eu-west-1")


@pytest.fixture
def resource():
    return boto3.resource("ec2", region_name="eu-west-1")


def test_is_ignorable_true():
    tags = [
        {"Key": "foo", "Value": "bar"},
        {"Key": instances.SANDMAN_TAG, "Value": instances.IGNORE_TAG},
    ]
    assert instances.__is_ignorable(tags) is True


def test_is_ignorable_no_tag():
    tags = []
    assert instances.__is_ignorable(tags) is False


def test_is_ignorable_tag_wrong_value():
    tags = [{"Key": instances.SANDMAN_TAG, "Value": "foobar"}]
    assert instances.__is_ignorable(tags) is False


def test_is_ignorable_tag_wrong_key():
    tags = [{"Key": "foobar", "Value": instances.IGNORE_TAG}]
    assert instances.__is_ignorable(tags) is False


@mock_ec2
def test_retrieve_instances_all(client, resource):
    num_instances = 3
    resource.create_instances(
        ImageId="ami-xxxx",
        MinCount=num_instances,
        MaxCount=num_instances,
        InstanceType="t2.micro",
    )
    response = instances.__retrieve_instances(client)
    assert len(response) == num_instances


@mock_ec2
def test_retrieve_instances_no_instances(client):
    response = instances.__retrieve_instances(client)
    assert len(response) == 0


@mock_ec2
def test_retrieve_instances_instances_none_ignored(client, resource):
    num_instances = 5
    resource.create_instances(
        ImageId="ami-xxxx",
        MinCount=num_instances,
        MaxCount=num_instances,
        InstanceType="t2.micro",
        TagSpecifications=[
            {
                "ResourceType": "instance",
                "Tags": [{"Key": "foo", "Value": "bar"}],
            },
        ],
    )
    response = instances.__retrieve_instances(client)
    assert len(response) == num_instances


@mock_ec2
def test_retrieve_instances_instances_all_ignored(client, resource):
    num_instances = 2
    resource.create_instances(
        ImageId="ami-xxxx",
        MinCount=num_instances,
        MaxCount=num_instances,
        InstanceType="t2.micro",
        TagSpecifications=[
            {
                "ResourceType": "instance",
                "Tags": [
                    {
                        "Key": instances.SANDMAN_TAG,
                        "Value": instances.IGNORE_TAG,
                    }
                ],
            },
        ],
    )
    response = instances.__retrieve_instances(client)
    assert len(response) == 0


@mock_ec2
def test_retrieve_instances_instances_half_ignored(client, resource):
    num_instances = 10
    resource.create_instances(
        ImageId="ami-xxxx",
        MinCount=num_instances,
        MaxCount=num_instances,
        InstanceType="t2.micro",
        TagSpecifications=[
            {
                "ResourceType": "instance",
                "Tags": [
                    {
                        "Key": instances.SANDMAN_TAG,
                        "Value": instances.IGNORE_TAG,
                    }
                ],
            },
        ],
    )
    resource.create_instances(
        ImageId="ami-xxxx",
        MinCount=num_instances,
        MaxCount=num_instances,
        InstanceType="t2.micro",
    )
    response = instances.__retrieve_instances(client)
    assert len(response) == num_instances


@mock_ec2
def test_start_instances(resource):
    num_instances = 3
    resource.create_instances(
        ImageId="ami-xxxx",
        MinCount=num_instances,
        MaxCount=num_instances,
        InstanceType="t2.micro",
    )
    response = instances.start_instances()
    assert response["status_code"] == 200
    assert (
        f"Started {num_instances} instances successfully" in response["body"]
    )


@mock_ec2
def test_stop_instances(resource):
    num_instances = 5
    resource.create_instances(
        ImageId="ami-xxxx",
        MinCount=num_instances,
        MaxCount=num_instances,
        InstanceType="t2.micro",
    )
    response = instances.stop_instances()
    assert response["status_code"] == 200
    assert (
        f"Stopped {num_instances} instances successfully" in response["body"]
    )
