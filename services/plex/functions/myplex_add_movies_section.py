"""Serverless Lambda - plexapi"""
from plexapi.exceptions import NotFound
from helpers import get_plex_server


def handler(event, context):
    """Use PlexApi to set up plex ec2 server and MyPlex account"""
    print('event in: ', event)
    token = event["token"]
    plex_server = get_plex_server(token)
    try:
        plex_server.library.section('Movies')
        print('Movies section already exists. moving on...')
        event['movies_existed'] = True
    except NotFound:
        print('adding movies section...')
        event['movies_existed'] = False
        plex_server.library.add(
            "Movies", "movie", "com.plexapp.agents.imdb", "Plex Movie Scanner", "/movies")
    section = plex_server.library.section('Movies')
    event[section.title] = True if section.title else False
    print('event out: ', event)
    return event
