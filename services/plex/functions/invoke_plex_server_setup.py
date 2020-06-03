"""Serverless Lambda - invoke plex server setup step function"""
import os
import json
import boto3

stepfunctions = boto3.client('stepfunctions')


def handler(event, context):
    """invoke step function handler"""
    step_function_arn = os.environ['plexServerSetupStepArn']
    print('step_function_arn', step_function_arn)
    response = stepfunctions.start_execution(
        stateMachineArn=step_function_arn,
        input=json.dumps({'lambda_invoked': True})
    )

    print('event', event)
    print('response', response)

    return True
