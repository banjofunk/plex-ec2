// eslint-disable-next-line import/no-unresolved
const AWS = require('aws-sdk');

const cloudformation = new AWS.CloudFormation();

module.exports = async stackNameInp => {
  const stackName = stackNameInp || `plex-vpc-ec2-${process.env.stage}`;

  return cloudformation
    .describeStacks({
      StackName: stackName,
    })
    .promise()
    .then(({ Stacks: [{ Outputs: outputs }] }) => {
      const outputsObj = {};

      for (const { OutputKey, OutputValue } of outputs) {
        outputsObj[OutputKey] = OutputValue;
      }

      return outputsObj;
    });
};
