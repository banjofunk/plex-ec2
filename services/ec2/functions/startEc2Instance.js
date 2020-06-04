// eslint-disable-next-line import/no-unresolved
const AWS = require('aws-sdk');
const getOutputs = require('../helpers/getOutputs');

const ec2 = new AWS.EC2();

module.exports.handler = async (event, context) => {
  const { PlexEc2InstanceId: plexEc2InstanceId } = await getOutputs();

  console.log('Starting ec2:', plexEc2InstanceId);
  const params = {
    InstanceIds: [plexEc2InstanceId],
  };
  const ec2Resp = await ec2
    .startInstances(params)
    .promise()
    .then(response => ({
      statusCode: 200,
      body: JSON.stringify({ response }),
    }))
    .catch(err => {
      console.error(err);

      return err;
    });

  console.log('ec2Resp', ec2Resp);

  return ec2Resp;
};
