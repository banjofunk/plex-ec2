// eslint-disable-next-line import/no-unresolved
const AWS = require('aws-sdk');
const fs = require('fs');

const s3 = new AWS.S3({ apiVersion: '2006-03-01' });

const uploadTemplates = async () => {
  const templatePath = `${__dirname}/plex_vpc_ec2.yml`;

  const fileContent = fs.readFileSync(templatePath, { encoding: 'utf8', flag: 'r' });

  const params = {
    Bucket: 'plex-movie',
    Key: 'plex_vpc_ec2.yml',
    Body: fileContent,
  };

  const url = await s3
    .upload(params)
    .promise()
    .then(({ Location }) => Location)
    .catch(console.error);

  console.log('url', url);

  return {
    statusCode: 200,
    body: JSON.stringify({ url }),
  };
};

uploadTemplates();
