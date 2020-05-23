"""Serverless Lambda - plexapi"""
import os
from helpers import get_myplex_account


def handler(event, context):
    """Use PlexApi to remove old plex ec2 servers and MyPlex devices"""
    account = get_myplex_account()
    for device in account.devices():
        print('device.name', device.name)
        print('device.product', device.product)
        print('device.platform', device.platform)
        if (device.name == 'Plex-Ec2'):
            print(f"removing old Plex-Ec2 instance:", device.name)
            # device.delete()
        if (device.name != os.environ['plexIp']) and (device.product == 'PlexAPI'):
            print(f"removing old Plex-Ec2 instance:", device.name)

    event['cleaned'] = True
    return event
