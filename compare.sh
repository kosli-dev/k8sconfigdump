#!/bin/bash

set -e

# Check if the filenames arguments are provided
if [ $# -ne 2 ]; then
    echo "Please provide two filenames of YAML files as arguments."
    exit 1
fi

source_yaml=$1
downloaded_yaml=$2

# Check if the files exist
if [ ! -f "$source_yaml" ]; then
    echo "File '$source_yaml' does not exist."
    exit 1
fi

if [ ! -f "$downloaded_yaml" ]; then
    echo "File '$downloaded_yaml' does not exist."
    exit 1
fi

# convert both files to JSON using yq
source_json=$(yq --unwrapScalar $source_yaml -o json)
downloaded_json=$(yq --unwrapScalar $downloaded_yaml -o json)

#echo "source is: $source_json"
#echo "downloaded is: $downloaded_json"

# sort both JSON files
sorted_source_json=$(echo $source_json | jq -S .)
sorted_downloaded_json=$(echo $downloaded_json | jq -S .)

# logical diff the sorted JSON files with jq
diff=$(echo $sorted_source_json $sorted_downloaded_json | jq -S 'diff' | jq -r '.[] | select(.value != null) | .key')

echo $diff
