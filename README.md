# plex-ec2

plex-ec2 uses the serverless framework to deploy and manage Plex Media Server on  AWS EC2. Media is stored in S3 and mounted with s3-fs. Since ec2 uptime and reserved ip addresses are billed, step functions manage:
  - starting and stoping ec2 instances
  - attaching and releasing ip addresses
  - associating plex-ec2 with your my-plex account


## clone and deploy
```bash
# use your aws keys
export AWS_PROFILE=<AWS_PROFILE_NAME>

#clone the repo
git clone git@github.com:banjofunk/plex-ec2.git

cd plex-ec2
npm install

#aws cli to put plex credentials in AWS SSM parameter store
npm run set-username <PLEX-USERNAME> #Stored as String
npm run set-password <PLEX-PASSWORD> #Stored as SecureString

#serverless framework / cloudformation. check the deploy script.
npm run deploy
```

## Usage
```bash
# stops ec2 instance and releases IP
npm run plex-down

# start ec2 / attach ip / claim plex server / myplex login
npm run plex-up

# remove it all
npm run undeploy
```
## AWS Diagram
![AWS Diagram](/assets/images/aws-diagram.png)

## Plex Up Step Function Diagram
![AWS Diagram](/assets/images/plex-up-step.png)
