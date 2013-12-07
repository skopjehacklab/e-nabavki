#!/bin/bash
#
# Downloads all links from one page. Invoked by initial_get_all_links.sh
#

page=$1
file=$2
if [ ! -f "$file" ]; then
	echo casperjs e-nabavki.gov.mk.js --page=$page "to" "$file"
	casperjs e-nabavki.gov.mk.js --page=$page > "$file"
fi

