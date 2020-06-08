"""Serverless Lambda - invoke plex server setup step function"""
import os
import boto3
from botocore.exceptions import ClientError
client = boto3.client('cloudformation')


def handler(event, context):
    """invoke step function handler"""
    stack_name = f"plex-vpc-ec2-{os.environ['stage']}"

    try:
        data = client.describe_stacks(StackName=stack_name)
        event['createStackStatus'] = data['Stacks'][0]['StackStatus']
    except ClientError:
        event['createStackStatus'] = "NO_STACK"

    return event
