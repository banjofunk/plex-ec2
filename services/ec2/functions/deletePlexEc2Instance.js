// eslint-disable-next-line import/no-unresolved
const AWS = require('aws-sdk');

const cloudformation = new AWS.CloudFormation();

module.exports.handler = async (event, context) => {
  const params = { StackName: `plex-vpc-ec2-${process.env.stage}` };
  const cloudformationResponse = await cloudformation
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

  // await cloudformation
  //   .waitFor('stackDeleteComplete', params)
  //   .promise()
  //   .then(console.log)
  //   .catch(console.error);

  console.log('cloudformationResponse:', cloudformationResponse);

  return cloudformationResponse;
};
