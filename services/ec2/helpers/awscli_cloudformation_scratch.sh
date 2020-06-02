aws cloudformation list-exports --stack-name "plex-vpc-ec2-dev" 

aws cloudformation describe-stacks --stack-name "plex-vpc-ec2-dev" 

aws cloudformation describe-stacks --stack-name plex-vpc-ec2-dev | 
  jq -c '.Stacks[].Outputs[] | select( .OutputKey | contains ("PlexEc2InstanceId")).OutputValue'


aws cloudformation delete-stack --stack-name "plex-vpc-ec2-dev" 


aws cloudformation create-stack \
  --stack-name "plex-vpc-ec2-dev" \
  --capabilities CAPABILITY_NAMED_IAM \
  --template-url https://plex-movie.s3.amazonaws.com/plex_vpc_ec2.yml \
  --parameters ParameterKey=AvailabilityZone,ParameterValue=us-west-2a \
    ParameterKey=ApiEndpoint,ParameterValue="https://ga9fmoqsdc.execute-api.us-west-2.amazonaws.com/dev" 

aws cloudformation update-stack \
  --stack-name "plex-vpc-ec2-dev" \
  --capabilities CAPABILITY_NAMED_IAM \
  --template-url https://plex-movie.s3.amazonaws.com/plex_vpc_ec2.yml \
  --parameters ParameterKey=AvailabilityZone,ParameterValue=us-west-2a \
    ParameterKey=ApiEndpoint,ParameterValue="https://ga9fmoqsdc.execute-api.us-west-2.amazonaws.com/dev" 


#TODO =============>>>> Check if stack create is complete for step function. retry.