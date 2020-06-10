"""Serverless Lambda - invoke plex server setup step function"""
import boto3
from helpers import get_outputs
client = boto3.client('ec2')


def handler(event, context):
    """invoke step function handler"""
    outputs = get_outputs()

    response = client.start_instances(
        InstanceIds=[
            outputs['PlexEc2InstanceId'],
        ],
    )

    print('event', event)
    print('response', response)

    return event
