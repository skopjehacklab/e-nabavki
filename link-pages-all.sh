page=0
while [[ $page -lt 3500 ]]; do 
	echo "$page" 
	echo "pages/$page.json"; 
	page=$(($page + 1));
done | xargs -n 2 -P 8 ./link-page-get.sh

