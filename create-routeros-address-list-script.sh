#!/bin/bash
term_colors() {
    red=`tput setaf 1`
    green=`tput setaf 2`
    yellow=`tput setaf 3`
    blue=`tput setaf 4`
    magenta=`tput setaf 5`
    cyan=`tput setaf 6`
    white=`tput setaf 7`
    reset=`tput sgr0`
    blink=`tput blink`
}
term_colors

LINUX=0
ADDRESS_LIST="Blacklist"
#/ip/firewall/address-list/print file=sdcard/list.txt where list="drop_traffic"

if [[ $# -eq 0 ]]; then
	USE_IP_TXT=1
	echo "Using ip.txt as a list of JUST IPs!!!!"
	sleep 5s
else
	USE_IP_TXT=0
fi

if [[ $LINUX -eq 1 ]]; then
	SCRIPT_FILE="newip.sh"
else
	SCRIPT_FILE="newip.ps1"
fi

rm $SCRIPT_FILE 2>/dev/null > /dev/null
if [[ $USE_IP_TXT -eq 0 ]]; then
	rm ip.txt 2>/dev/null > /dev/null
	#rm newip.ps1 2>/dev/null > /dev/null
	#if exported from print use field 7
	cat "$1" | egrep '^.[0-9].*drop_traffic.*' | tr -s ' ' | \
	sed 's/^ \(.*\)/\1/g' | cut -d$' ' -f4 |sort -n|uniq > ip.txt
	#cat "$1" | cut -d$' ' -f5 |sort -n > ip.txt

	#if exported with export, use field 5
	#cat "$1" | cut -d' ' -f5|sort -n > ip.txt
fi
if [[ $LINUX -eq 1 ]]; then
	echo "#!/bin/bash" > $SCRIPT_FILE
fi
if [[ 1 -eq 2 ]]; then
	cat ip.txt | xargs -I {} echo ./check-ip.py -l $ADDRESS_LIST -i {} >> $SCRIPT_FILE
else
	COUNTER=1
	TTL_LINES=`cat ip.txt | wc -l`
	RESULTS=`cat ip.txt`
	while IFS= read -r ip; do
		echo "Write-Host \"Processing ${COUNTER} of ${TTL_LINES}\" -ForegroundColor Green" >> $SCRIPT_FILE
		echo ./check-ip.py -l $ADDRESS_LIST -i ${ip} >> $SCRIPT_FILE
		COUNTER=`echo "${COUNTER} + 1" | bc`
	done <<< "$RESULTS"
fi
if [[ $LINUX -eq 1 ]]; then
	chmod +x $SCRIPT_FILE
fi


