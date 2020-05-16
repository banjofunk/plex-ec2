import boto3 
import re, json, os
from time import sleep
from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer
from plexapi.exceptions import NotFound

ssm = boto3.client('ssm')

def handler(event, context):
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
  account = MyPlexAccount(params['username'], params['password'])
  try:
    device = account.device('Plex-Ec2')
    device.delete()
    print('removed old Plex-Ec2 server.')
  except NotFound:
    print('no Plex-Ec2 servers found. moving on...')

  plexIp = os.environ['plexIp']
  baseurl = f"http://{plexIp}:32400"
  i = 0
  while True:
    try:
      plex = PlexServer(baseurl, account._token)
    except Exception as e:
      i += 1
      print(e)
      sleep(10)
      continue
    else:
      break

  plex.library.add("Movies", "movie", "com.plexapp.agents.imdb", "Plex Movie Scanner", "/movies")
  plex.settings.get("AcceptedEULA").set(True)
  plex.settings.get("PublishServerOnPlexOnlineKey").set(True)
  plex.settings.save()
  print(plex)
  print(plex.myPlex)
  response = {
    'statusCode': 200,
    'body': json.dumps({"myplex":plex.myPlex})
  }
 
  return response
