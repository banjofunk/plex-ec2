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

remove() {
    SERVICE=$1
    SERVICENAME="$(getServiceName $SERVICE)"

    echo "${orange}Removing $SERVICENAME${reset} service\n"
    cwd=$(pwd)
    cd $SERVICE
    serverless remove
    cd $cwd
    echo "${green}$SERVICENAME service removed.${reset}\n"
}

## Install service deps / Deploy services
for service in services/*/
do
    remove $service &
done
wait 
echo "${orange}Removing plex-ec2 resources.${reset}\n"
serverless remove
echo "${green}plex-ec2 resources removed.${reset}\n"

wait

echo "
***********************************************

Removal Complete! Check above for any ${red}errors${reset}.
"