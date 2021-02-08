#!/bin/bash

####Run script with: ./find_10_largest_files.sh -d /opt

get_input_dir(){
	local OPTIND
	while getopts ":d:" flag;
	do
   		 case "$flag" in
        		d) DIR=$OPTARG;;
    	esac
	done
}

check_if_dir_wasnt_set(){

echo "ROOT DIR: $DIR"
if [ -z "${DIR}" ]; then
    echo "DIR is unset or set to the empty string"
    exit 1
fi
}

###Main###
get_input_dir "$@"
check_if_dir_wasnt_set

sudo find $DIR -mount -type f -printf '%s %p\n' 2>/dev/null| sort -nr | head -10
