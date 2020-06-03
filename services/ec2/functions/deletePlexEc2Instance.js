// eslint-disable-next-line import/no-unresolved
const AWS = require('aws-sdk');

const cloudformation = new AWS.CloudFormation();

module.exports.handler = async (event, context) => {
  const params = { StackName: `plex-vpc-ec2-${process.env.stage}` };
  const cloudformationResp = await cloudformation
    .deleteStack(params)
    .promise()
    .then(response => ({
      statusCode: 200,
      body: JSON.stringify({ response }),
    }))
    .catch(err => {
      console.error(err);

      return err;
    });

  console.log('cloudformationResp:', cloudformationResp);

  return cloudformationResp;
};
