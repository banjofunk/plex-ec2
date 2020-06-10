"""Serverless Lambda - invoke plex server setup step function"""
import os
import boto3
from helpers import get_stack_params
client = boto3.client('cloudformation')


def handler(event, context):
    """invoke step function handler"""
    stack_params = get_stack_params()
    if stack_params['WithIpAddress'] == 'true':
        event['updateStackStatus'] = 'ALREADY_ATTACHED'
    else:
        try:
            response = client.update_stack(
                StackName=f"plex-vpc-ec2-{os.environ['stage']}",
                TemplateURL='https://plex-movie.s3.amazonaws.com/plex_vpc_ec2.yml',
                Parameters=[
                    {
                        'ParameterKey': 'AvailabilityZone',
                        'ParameterValue': os.environ['availabilityZone'],
                    },
                    {
                        'ParameterKey': 'WithIpAddress',
                        'ParameterValue': 'true',
                    },
                ],
                Capabilities=[
                    'CAPABILITY_NAMED_IAM',
                ],
            )

            print('response', response)
            event['updateStackStatus'] = 'UPDATE_IN_PROGRESS'
        except:
            event['updateStackStatus'] = 'UPDATE_ERROR'

    return event
