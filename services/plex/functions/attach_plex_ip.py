"""Serverless Lambda - invoke plex server setup step function"""
import os
import boto3
from botocore.exceptions import ClientError
from helpers import get_params, get_outputs
client = boto3.client('ec2')
ssm_client = boto3.client('ssm')


def handler(event, context):
    """invoke step function handler"""
    params = get_params()
    outputs = get_outputs()

    print('plex-ip', params['plex-ip'])
    print('outputs', outputs['PlexEc2InstanceId'])

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
            event['ipAttachStatus'] = 'IP_ALREADY_ATTACHED'
        else:
            allocate_response = client.allocate_address()
            print('allocate_response', allocate_response)
            associate_response = client.associate_address(
                AllocationId=allocate_response['AllocationId'],
                InstanceId=outputs['PlexEc2InstanceId']
            )
            print('associate_response', associate_response)
            ssm_client.put_parameter(
                Name='/plex-ec2/plex-ip',
                Value=allocate_response['PublicIp'],
                Type='String',
                Overwrite=True,
            )
            event['AssociationId'] = associate_response['AssociationId']
            event['AllocationId'] = allocate_response['AllocationId']
            event['PlexIp'] = allocate_response['PublicIp']
            event['ipAttachStatus'] = 'IP_ATTACHED'
    except ClientError:
        event['ipAttachStatus'] = 'IP_ATTACH_ERROR'

    return event
