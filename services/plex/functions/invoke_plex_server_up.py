"""Serverless Lambda - invoke plex server setup step function"""
import os
import json
import boto3
stepfunctions = boto3.client('stepfunctions')


def handler(event, context):
    """invoke step function handler"""
    try:
        response = stepfunctions.start_execution(
            stateMachineArn=os.environ['plexServerUpStepArn'],
            input=json.dumps({'lambda_invoked': True})
        )
    except:
        return False

    print('event', event)
    print('response', response)

    return response['executionArn']
