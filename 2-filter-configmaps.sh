#!/bin/bash

set -e

# Usage:
# ./2-snapshot-configmaps.sh 
#
# 

source env/bin/activate

rm -rf /tmp/snapdir
mkdir -p /tmp/snapdir
python src/filter_configmaps.py /tmp/snapdir