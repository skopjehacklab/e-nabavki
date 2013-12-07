#!/bin/bash
#
# Initial multiprocess resumable parse of 3500 pages from e-nabavki
# to get all the dosie links.
#

if [ ! -d "pages/" ]; then
    mkdir pages
fi;

page=0
while [[ $page -lt 3500 ]]; do 
	echo "$page" 
	echo "pages/$page.json"; 
	page=$(($page + 1));
done | xargs -n 2 -P 8 ./link-page-get.sh

