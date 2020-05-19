// eslint-disable-next-line import/no-unresolved
const AWS = require('aws-sdk');

const ssm = new AWS.SSM();
const fetch = require('node-fetch');
const getParams = require('../helpers/getParams');

module.exports.handler = async (event, context) => {
  const { username, password } = await getParams();
  const associateClaimTokenUrl = `${process.env.apiBaseUrl}/associate-claim-token`;

  console.log('associateClaimTokenUrl', associateClaimTokenUrl);

  const params = {
    DocumentName: 'AWS-RunShellScript',
    CloudWatchOutputConfig: {
      CloudWatchLogGroupName: context.logGroupName,
      CloudWatchOutputEnabled: true,
    },
    Comment: 'set plex claim token and start plex media server',
    InstanceIds: [process.env.PlexEc2InstanceId],
    Parameters: {
      commands: [
        'cd /home/ec2-user',
        'docker stop $(docker ps -a -q)',
        'docker rm $(docker ps -a -q)',
        `auth_token=$(curl -X POST "https://plex.tv/users/sign_in.json?user[login]=${username}&user[password]=${password}&X-Plex-Client-Identifier=plex-ec2" | jq .user.authentication_token | tr -d '"')`,
        'echo "AUTH_TOKEN: $auth_token"',
        `claim_token=$(curl -L "https://plex.tv/api/claim/token.json?X-Plex-Token=$auth_token" | jq .token | tr -d '"')`,
        'echo "CLIENT_TOKEN: $claim_token"',
        `docker run \
          -d \
          --name plex \
          --restart unless-stopped \
          -p 32400:32400/tcp \
          -p 3005:3005/tcp \
          -p 8324:8324/tcp \
          -p 32469:32469/tcp \
          -p 1900:1900/udp \
          -p 32410:32410/udp \
          -p 32412:32412/udp \
          -p 32413:32413/udp \
          -p 32414:32414/udp \
          -e TZ="America/Los_Angeles" \
          -e PLEX_CLAIM="$claim_token" \
          -e ADVERTISE_IP=http://0.0.0.0:32400/ \
          -h Plex-Ec2 \
          -v /home/ec2-user/plex-config/config:/config \
          -v /home/ec2-user/plex-config/transcode:/transcode \
          -v /home/ec2-user/movies:/movies \
        plexinc/pms-docker`,
        'sleep 2',
        `curl -L "${associateClaimTokenUrl}/$auth_token"`,
      ],
    },
    TimeoutSeconds: 30,
  };
  const ssmResp = await ssm
    .sendCommand(params)
    .promise()
    .catch(console.error);

  console.log('Send Command params:', params);

  return {
    statusCode: 200,
    body: JSON.stringify({ response: ssmResp }),
  };
};
