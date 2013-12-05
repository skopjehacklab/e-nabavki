page=$1
file=$2
if [ ! -f "$file" ]
then	
	echo casperjs e-nabavki.gov.mk.js --page=$page "to" "$file"
	casperjs e-nabavki.gov.mk.js --page=$page > "$file"
	#sleep 6
fi

