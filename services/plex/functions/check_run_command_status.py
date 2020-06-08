"""Serverless Lambda - invoke plex server setup step function"""
import boto3
from helpers import get_outputs
client = boto3.client('ssm')


def handler(event, context):
    """invoke step function handler"""
    outputs = get_outputs()

    response = client.get_command_invocation(
        CommandId=event['commandId'],
        InstanceId=outputs['PlexEc2InstanceId'],
    )

    print('event', event)
    print('response', response)

    event['runCommandStatus'] = response['Status']

    return event
