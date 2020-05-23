"""Serverless Lambda - plexapi"""
from helpers import get_myplex_account


def handler(event, context):
    """Use PlexApi to set up plex ec2 server and MyPlex account"""
    account = get_myplex_account()
    token = account.authenticationToken
    event['token'] = token
    return event
