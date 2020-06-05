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

deploy() {
    SERVICE=$1
    SERVICENAME="$(getServiceName $SERVICE)"
    echo "${prefix} Deploying ${orange}$SERVICENAME${reset} service\n"
    cwd=$(pwd)
    cd $SERVICE
    npm install
    PYTHON_REQUIREMENTS=./requirements.txt
    if test -f "$PYTHON_REQUIREMENTS"; then
        pip install -r ./requirements.txt
    fi
    serverless deploy --stage $STAGE --region $REGION
    cd $cwd
}

## Install deps / Deploy resrouces
npm install
serverless deploy --stage $STAGE --region $REGION
deploy 'services/ec2'
deploy 'services/plex'

cwd=$(pwd)
cd 'services/ec2'
echo "${prefix} Creating ${orange}plex-vpc-ec2-$STAGE${reset} instance\n"
serverless invoke -f createPlexEc2Instance
aws cloudformation wait stack-create-complete --stack-name "plex-vpc-ec2-$STAGE"
echo "${prefix} Instance ${green}plex-vpc-ec2-$STAGE${reset} created\n"

echo "${prefix} ${orange}setting up plex server...${reset}\n"
serverless invoke -f setPlexClaimToken


cd $cwd

echo "

***********************************************

Deployment Complete! Check above for any ${red}errors${reset}.
"
