"""Serverless Lambda - plexapi"""
import re
import json
import os
from time import sleep
import boto3
from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer
from plexapi.exceptions import NotFound

ssm = boto3.client('ssm')


def get_params():
    """Get MyPlex username and password AWS from parameter store"""
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


def remove_old_devices(account):
    """Remove old Plex-Ec2 devices from MyPlex account"""
    for device in account.devices():
        if device.name == 'Plex-Ec2':
            print(f"removing old Plex-Ec2 instance.")
            device.delete()


def claim_plex_server(token):
    """Associate plex-ec2 server with MyPlex account"""
    plex_ip = os.environ['plexIp']
    baseurl = f"http://{plex_ip}:32400"
    print('baseurl', baseurl)
    plex_server = PlexServer(baseurl, token)
    print('plex_server', plex_server)
    return plex_server


def create_movies_section(plex_server):
    """Use existing movies section or create new"""
    try:
        plex_server.library.section('Movies')
        print('Movies section already exists. moving on...')
    except NotFound:
        print('adding movies section...')
        plex_server.library.add(
            "Movies", "movie", "com.plexapp.agents.imdb", "Plex Movie Scanner", "/movies")


def update_server_settings(plex_server):
    """Update settings to accept terms and share server with MyPlex"""
    plex_server.settings.get("AcceptedEULA").set(True)
    plex_server.settings.get("PublishServerOnPlexOnlineKey").set(True)
    plex_server.settings.save()
    print('saved settings.', plex_server)


def handler(event, context):
    """Use PlexApi to set up plex ec2 server and MyPlex account"""
    token = event['pathParameters']['token']
    print('TOKEN:', token)
    params = get_params()
    account = MyPlexAccount(params['username'], params['password'])
    print('account:', account)
    remove_old_devices(account)
    sleep(20)
    plex_server = claim_plex_server(token)
    create_movies_section(plex_server)
    update_server_settings(plex_server)
    sections = plex_server.library.sections()
    print(sections)
    sleep(5)

    return {
        'statusCode': 200,
        'body': json.dumps({'updated': True})
    }
