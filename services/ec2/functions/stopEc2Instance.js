// eslint-disable-next-line import/no-unresolved
const AWS = require('aws-sdk');

const ec2 = new AWS.EC2();

module.exports.handler = async (event, context) => {
  const params = {
    InstanceIds: ['i-0f754c245559df22c'],
  };

  const ec2Resp = await ec2
    .stopInstances(params)
    .promise()
    .catch(console.error);

  console.log('Stop Instances params:', params);

  return {
    statusCode: 200,
    body: JSON.stringify({ response: ec2Resp }),
  };
};
