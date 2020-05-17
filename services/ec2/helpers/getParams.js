// eslint-disable-next-line import/no-unresolved
const AWS = require('aws-sdk');

const ssm = new AWS.SSM();

module.exports = async () => {
  const path = `/plex-ec2/`;

  return ssm
    .getParametersByPath({
      Path: path,
      WithDecryption: true,
    })
    .promise()
    .then(data => {
      const params = {};

      data.Parameters.forEach(param => {
        const name = param.Name.replace(path, '');

        params[name] = param.Value;
      });

      return params;
    });
};
