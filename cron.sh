#!/bin/bash

now=$(date +'%Y%m%d')

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
base_file=$DIR'/time.log'
destination=$DIR'/data/'$now'.csv'

[ -f $base_file ] && mv $base_file $destination
