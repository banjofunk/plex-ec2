"""plexapi - helpers module"""
import re
import os
import boto3
from plexapi.server import PlexServer
from plexapi.myplex import MyPlexAccount

ssm = boto3.client('ssm')
cloudformation = boto3.client('cloudformation')


def get_outputs():
    """Get MyPlex username and password AWS from parameter store"""
    stack_name = f"plex-vpc-ec2-{os.environ['stage']}"
    cloudformation_response = cloudformation.describe_stacks(
        StackName=stack_name
    )
    cloudformation_outputs = cloudformation_response['Stacks'][0]['Outputs']
    outputs = {}
    for output in cloudformation_outputs:
        key = output["OutputKey"]
        value = output["OutputValue"]
        outputs[key] = value
    return outputs


def get_params():
    """Get params AWS from parameter store"""
    ssm_response = ssm.get_parameters_by_path(
        Path='/plex-ec2/',
        WithDecryption=True
    )
    params = {}
    for parameter in ssm_response['Parameters']:
        name = parameter["Name"]
        prefix = re.search("/plex-ec2/", name)
        key = name[prefix.end():]
        params[key] = parameter["Value"]
    return params


def get_myplex_account():
    """Use PlexApi to set up plex ec2 server and MyPlex account"""
    params = get_params()
    account = MyPlexAccount(params['username'], params['password'])
    return account


def get_plex_server(token):
    """Associate plex-ec2 server with MyPlex account"""
    outputs = get_outputs()
    plex_ip = outputs['PlexIp']
    baseurl = f"http://{plex_ip}:32400"
    print('baseurl', baseurl)
    plex_server = PlexServer(baseurl, token)
    print('plex_server', plex_server)
    return plex_server
