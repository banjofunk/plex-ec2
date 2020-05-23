"""Serverless Lambda - plexapi"""
from helpers import get_plex_server


def handler(event, context):
    """Update settings to accept terms and share server with MyPlex"""
    print('event in: ', event)
    token = event["token"]
    plex_server = get_plex_server(token)
    plex_server.settings.get("AcceptedEULA").set(True)
    plex_server.settings.get("PublishServerOnPlexOnlineKey").set(True)
    plex_server.settings.save()
    print('saved settings.')
    event['initialied'] = True if plex_server else False
    print('event out: ', event)
    return event
