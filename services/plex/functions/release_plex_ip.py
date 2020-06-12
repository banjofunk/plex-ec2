"""Serverless Lambda - invoke plex server setup step function"""
import os
import boto3
from botocore.exceptions import ClientError
from helpers import get_params, get_outputs
client = boto3.client('ec2')


def handler(event, context):
    """invoke step function handler"""
    params = get_params()
    outputs = get_outputs()

    try:
        response = client.describe_addresses(
            Filters=[
                {
                    'Name': 'instance-id',
                    'Values': [
                        outputs['PlexEc2InstanceId']
                    ]
                },
            ]
        )

        if (response['Addresses']):
            event['AssociationId'] = response['Addresses'][0]['AssociationId']
            event['AllocationId'] = response['Addresses'][0]['AllocationId']

            client.disassociate_address(AssociationId=event['AssociationId'])
            client.release_address(AllocationId=event['AllocationId'])
            event['ipReleaseStatus'] = 'IP_RELEASED'
        else:
            event['ipReleaseStatus'] = 'IP_ALREADY_RELEASED'

    except ClientError:
        event['ipReleaseStatus'] = 'IP_RELEASE_ERROR'

    return event
