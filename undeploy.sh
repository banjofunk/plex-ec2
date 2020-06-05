#!/usr/bin/env bash

## Set up colors
red=$(tput setaf 1)
green=$(tput setaf 28)
orange=$(tput setaf 3)
reset=$(tput sgr0)

prefix="${orange}Plex Ec2:${reset}"

## Default Settings
STAGE="dev"
REGION="us-west-2"

getServiceName() {
    IFS='/'
    read -ra ADDR <<< "$1"
    SERVICENAME="${ADDR[@]: -1}"
    IFS=' '
    echo $SERVICENAME
}

remove() {
    SERVICE=$1
    SERVICENAME="$(getServiceName $SERVICE)"

    echo "${prefix} Removing ${orange}$SERVICENAME${reset} service\n"
    cwd=$(pwd)
    cd $SERVICE
    serverless remove
    cd $cwd
    echo "${prefix} Service ${green}$SERVICENAME${reset} removed.\n"
}


echo "${orange}removing plex-vpc-ec2 instance...${reset}\n"

aws cloudformation delete-stack \
  --stack-name "plex-vpc-ec2-$STAGE" \
  --output text >/dev/null

aws cloudformation wait stack-delete-complete \
  --stack-name "plex-vpc-ec2-$STAGE"

echo "${prefix} Instance ${green}plex-vpc-ec2-$STAGE${reset} removed\n"

remove 'services/ec2'
remove 'services/plex'

serverless remove
echo "${prefix} Resource ${green}plex-vpc-ec2-resrouces-$STAGE ${reset}removed\n"

wait

echo "
***********************************************

Removal Complete! Check above for any ${red}errors${reset}.
"
