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
        response = client.describe_instance_status(
            InstanceIds=[
                outputs['PlexEc2InstanceId'],
            ],
        )
        print(response)
        all_statuses = response['InstanceStatuses'][0]
        instance_status = all_statuses['InstanceState']['Name']
        status_checks_ok = all_statuses['InstanceStatus']['Status'] == 'ok' and all_statuses['SystemStatus']['Status'] == 'ok'

        event['instanceStatus'] = 'STATUS_NOT_OK'
        if instance_status == 'running' and status_checks_ok:
            event['instanceStatus'] = 'STATUS_OK'

    except ClientError:
        event['instanceStatus'] = "STATUS_ERROR"

    return event
