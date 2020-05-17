// eslint-disable-next-line import/no-unresolved
const AWS = require('aws-sdk');

const ssm = new AWS.SSM();
const fetch = require('node-fetch');
const getParams = require('../helpers/getParams');

module.exports.handler = async (event, context) => {
  const { username, password } = await getParams();
  const { Host: urlHost } = event.headers;
  const associateClaimTokenUrl = `https://${urlHost}/${process.env.stage}/associate-claim-token`;

  const plexUserAuthToken = await fetch(
    `https://plex.tv/users/sign_in.json?user[login]=${username}&user[password]=${password}&X-Plex-Client-Identifier=plex-ec2`,
    {
      method: 'post',
    }
  )
    .then(resp => resp.json())
    .then(({ user: { authToken } }) => authToken)
    .catch(console.error);

  const plexClaimToken = await fetch(`https://plex.tv/api/claim/token.json?X-Plex-Token=${plexUserAuthToken}`)
    .then(resp => resp.json())
    .then(({ token }) => token)
    .catch(console.error);

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
        'docker stop plex',
        'docker rm plex',
        `echo PLEX_CLAIM=${plexClaimToken} > .env`,
        '/usr/local/bin/docker-compose -p plex up -d',
        'sleep 20',
        `curl -L '${associateClaimTokenUrl}'`,
      ],
    },
    TimeoutSeconds: 30,
  };
  const ssmResp = await ssm
    .sendCommand(params)
    .promise()
    .catch(console.error);

  console.log('Send Command:', ssmResp);

  return {
    statusCode: 200,
    body: JSON.stringify({ response: ssmResp }),
  };
};
