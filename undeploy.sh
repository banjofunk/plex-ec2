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

remove() {
  service_path=$1
  service_name=" $(echo $service_path | sed s/\.\\/services\\///)"
  echo "${prefix} Removing ${orange}$service_name${reset} service\n"
  pushd $service_path
  serverless remove
  popd
  echo "${prefix} Service ${green}$service_name${reset} removed.\n"
}

echo "${orange}removing plex-vpc-ec2 instance...${reset}\n"
npm run plex-down
echo "${prefix} Instance ${green}plex-vpc-ec2-$STAGE${reset} removed\n"
echo "${prefix} Removing ${orange}all${reset} services\n"
for service in ./services/*; do remove $service; done

serverless remove
echo "${prefix} Resource ${green}plex-vpc-ec2-resouces-$STAGE ${reset}removed\n"

wait

echo "
***********************************************

Removal Complete! Check above for any ${red}errors${reset}.
"
