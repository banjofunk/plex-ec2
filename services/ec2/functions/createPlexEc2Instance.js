// eslint-disable-next-line import/no-unresolved
const AWS = require('aws-sdk');

const cloudformation = new AWS.CloudFormation();

module.exports.handler = async (event, context) => {
  const params = {
    StackName: `plex-vpc-ec2-${process.env.stage}`,
    TemplateURL: 'https://plex-movie.s3.amazonaws.com/plex_vpc_ec2.yml',
    Capabilities: ['CAPABILITY_NAMED_IAM'],
    Parameters: [
      {
        ParameterKey: 'AvailabilityZone',
        ParameterValue: process.env.availabilityZone,
      },
    ],
  };

  const resp = await cloudformation
    .createStack(params)
    .promise()
    .then(response => ({
      statusCode: 200,
      body: JSON.stringify({ response }),
    }))
    .catch(err => {
      console.error(err);

      return err;
    });

  console.log('resp', resp);

  return resp;
};
