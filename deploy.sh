#!/usr/bin/env bash

## Set up colors
red=$(tput setaf 1)
green=$(tput setaf 2)
orange=$(tput setaf 3)
reset=$(tput sgr0)

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

    echo "${green}Deploying $SERVICENAME${reset}\n"
    cwd=$(pwd)
    cd $SERVICE
    yarn install
    PYTHON_REQUIREMENTS=./requirements.txt
    if test -f "$PYTHON_REQUIREMENTS"; then
        pip install -r ./requirements.txt
    fi
    serverless deploy --stage $STAGE --region $REGION
    cd $cwd
}

## Install deps / Deploy resrouces
yarn install
serverless deploy --stage $STAGE --region $REGION
deploy 'services/ec2'
deploy 'services/plex'

cwd=$(pwd)
cd 'services/ec2'
serverless invoke -f createPlexEc2Instance
cd $cwd

echo "

***********************************************

Deployment Complete! Check above for any ${red}errors${reset}.
"
