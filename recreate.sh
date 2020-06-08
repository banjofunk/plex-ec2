#!/usr/bin/env bash

npm run plex-delete;
aws cloudformation wait stack-delete-complete --stack-name "plex-vpc-ec2-dev"; 
npm run upload-templates;
npm run plex-create;
