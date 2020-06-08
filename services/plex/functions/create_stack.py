"""Serverless Lambda - invoke plex server setup step function"""
import os
import boto3
from botocore.exceptions import ClientError
client = boto3.client('cloudformation')


def handler(event, context):
    """invoke step function handler"""
    response = client.create_stack(
        StackName=f"plex-vpc-ec2-{os.environ['stage']}",
        TemplateURL='https://plex-movie.s3.amazonaws.com/plex_vpc_ec2.yml',
        Parameters=[
            {
                'ParameterKey': 'AvailabilityZone',
                'ParameterValue': os.environ['availabilityZone'],
            },
        ],
        Capabilities=[
            'CAPABILITY_NAMED_IAM',
        ],
    )

    print('response', response)
    event['createStackStatus'] = 'CREATING_COMPLETE'

    return event
