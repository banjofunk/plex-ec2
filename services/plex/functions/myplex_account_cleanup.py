"""Serverless Lambda - plexapi"""
from helpers import get_myplex_account
from helpers import get_outputs


def handler(event, context):
    """Use PlexApi to remove old plex ec2 servers and MyPlex devices"""
    outputs = get_outputs()
    print('outputs', outputs)

    account = get_myplex_account()
    print('account', account)
    for device in account.devices():
        if (device.name == 'Plex-Ec2'):
            try:
                device.delete()
                print("removed old Plex-Ec2 instance:",
                      device.name, device.product, device.platform)
            except:
                print("ERROR removing old Plex-Ec2 instance:",
                      device.name, device.product, device.platform)
        if (device.name != outputs['PlexIp']) and (device.product == 'PlexAPI'):
            try:
                device.delete()
                print("removed old Plex-Ec2 instance:",
                      device.name, device.product, device.platform)
            except:
                print("ERROR removing old Plex-Ec2 instance:",
                      device.name, device.product, device.platform)

    event['cleaned'] = True
    return event
