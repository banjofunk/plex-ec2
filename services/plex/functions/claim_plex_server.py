"""Serverless Lambda - invoke plex server setup step function"""
import boto3
from helpers import get_outputs
client = boto3.client('ssm')


def handler(event, context):
    """invoke step function handler"""
    outputs = get_outputs()
    response = client.send_command(
        DocumentName='AWS-RunShellScript',
        InstanceIds=[
            outputs['PlexEc2InstanceId']
        ],
        Comment='set plex claim token and start plex media server',
        Parameters={
            'commands': [
                'cd /home/ec2-user'
                'docker stop $(docker ps -a -q)',
                'docker wait $(docker ps -a -q)',
                'docker rm $(docker ps -a -q)',
                """docker run -d \\
                    --name plex \\
                    --restart unless-stopped \\
                    -p 32400:32400/tcp \\
                    -p 3005:3005/tcp \\
                    -p 8324:8324/tcp \\
                    -p 32469:32469/tcp \\
                    -p 1900:1900/udp \\
                    -p 32410:32410/udp \\
                    -p 32412:32412/udp \\
                    -p 32413:32413/udp \\
                    -p 32414:32414/udp \\
                    -e TZ="America/Los_Angeles" \\
                    -e PLEX_CLAIM=""" + event["claimToken"] + """\\
                    -e ADVERTISE_IP=http://0.0.0.0:32400/ \\
                    -h plex-ec2 \\
                    -v /home/ec2-user/plex-config/config:/config \\
                    -v /home/ec2-user/plex-config/transcode:/transcode \\
                    -v /home/ec2-user/movies:/movies plexinc/pms-docker 
                """,
            ],
        },
        CloudWatchOutputConfig={
            'CloudWatchLogGroupName': context.log_group_name,
            'CloudWatchOutputEnabled': True,
        },
        TimeoutSeconds=30,
    )

    print('event before', event)
    print('response', response)
    event['commandId'] = response['Command']['CommandId']
    print('event after', event)

    return event
