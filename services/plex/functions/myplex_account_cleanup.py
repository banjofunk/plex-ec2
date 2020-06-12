"""Serverless Lambda - plexapi"""
from helpers import get_myplex_account
from helpers import get_params


def handler(event, context):
    """Use PlexApi to remove old plex ec2 servers and MyPlex devices"""
    params = get_params()
    device_name = params['plex-ip'] if 'plex-ip' in params else 'noplexip'

    try:
        account = get_myplex_account()
    except:
        print("error signing in to plex account")
        return {
            'statusCode': 500,
            'body': '{"error": "error signing in to plex account"}',
        }

    for device in account.devices():
        if (device.token != account.authenticationToken):
            if (device.name == 'plex-ec2'):
                device.delete()
                print("server --> removed old plex-ec2 server instance:",
                      device.name, device.product, device.platform)
            if (device.name != device_name) and (device.product == 'PlexAPI'):
                device.delete()
                print("removed old plex-ec2 api instance:",
                      device.name, device.product, device.platform)

    event['cleaned'] = True
    return event
