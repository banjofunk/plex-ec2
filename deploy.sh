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

deploy() {
  service_path=$1
  service_name=" $(echo $service_path | sed s/\.\\/services\\///)"
  echo "${prefix} Deploying ${orange}$service_name${reset} service\n"
  pushd $service_path
  npm install
  PYTHON_REQUIREMENTS=./requirements.txt
  if test -f "$PYTHON_REQUIREMENTS"; then
      pip install -r ./requirements.txt
  fi
  serverless deploy --stage $STAGE --region $REGION
  popd
  echo "${prefix} Service ${green}$service_name${reset} deployed.\n"
}

## Install deps / Deploy resouces
npm install
serverless deploy --stage $STAGE --region $REGION

echo "${prefix} Deploying ${orange}all${reset} services\n"
for service in ./services/*; do deploy $service; done

echo "${prefix} ${orange}setting up plex server...${reset}\n"
npm run plex-up

echo "

***********************************************

Deployment Complete! Check above for any ${red}errors${reset}.
"
