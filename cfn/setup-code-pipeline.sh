#!/usr/bin/env bash

PROPERTY_FILE_NAME=../conf/pipeline-configuration.properties
if [ -f "$PROPERTY_FILE_NAME" ]; then
    echo "property file found."
    while IFS='=' read -r key value
    do
    	echo "$key=${!key:-$value}"
    	export "$key=${!key:-$value}"
    	echo "${!key}"
    done < "$PROPERTY_FILE_NAME"
else
    echo "property file not found. Exiting."
    exit 1
fi

echo "\nCreating $CodePipelineStack ..."
aws cloudformation deploy --stack-name $CodePipelineStack \
--template-file ${CodePipelineStack}.yaml \
--capabilities CAPABILITY_NAMED_IAM \
--parameter-overrides \
ProjectName=$ProjectName