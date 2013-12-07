#!/bin/bash
#
# Initial multiprocess, resumable download and parse of the 3500 index 
# pages from e-nabavki to get all the dosie links on the the local filesystem.
#
# If invoked with an argument download only one page.
# If invoked without arguments start 8 parallel processes to get the links.
#
# When script finishes all the json files should be greater then 1000 bytes.
# cleanup with find and run it again.
#
# find pages/ -name "*.json" -size -1000c -ls -exec rm {} \;
#

# local dir of the script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PAGEDIR="${DIR}/pages"

if [ ! -d "${PAGEDIR}" ]; then
    mkdir "${PAGEDIR}"
fi;

if [ $# -lt 1 ]; then
    while [[ $pagenum -lt 3500 ]]; do 
	    echo "$pagenum";
	    pagenum=$(($pagenum + 1));
    done | xargs -n 1 -P 8 $0
else
    pagenum=$1
    filename="${PAGEDIR}/$1.json"

    if [ ! -f "$filename" ]; then
        echo casperjs e-nabavki.gov.mk.js --page=$pagenum "to" "$filename"
        casperjs ${DIR}/e-nabavki.gov.mk.js --page=$pagenum > "$filename"
    fi
fi

