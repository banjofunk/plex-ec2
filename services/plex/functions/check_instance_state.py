"""Serverless Lambda - invoke plex server setup step function"""
import os
import boto3
from botocore.exceptions import ClientError
from helpers import get_outputs
client = boto3.client('ec2')


def handler(event, context):
    """invoke step function handler"""
    outputs = get_outputs()

    try:
        response = client.describe_instances(
            InstanceIds=[
                outputs['PlexEc2InstanceId'],
            ],
        )
        instance = response['Reservations'][0]['Instances'][0]
        event['instanceState'] = instance['State']['Name']

    except ClientError:
        event['instanceStatus'] = "error"

    return event
