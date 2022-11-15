#!/bin/bash

LINUX=1
if [[ $LINUX -eq 1 ]]; then
	SCRIPT_FILE="newip.sh"
else
	SCRIPT_FILE="newip.ps1"
fi

ADDRESS_LIST="Blacklist"

rm ip.txt 2>/dev/null > /dev/null
#rm newip.ps1 2>/dev/null > /dev/null
rm $SCRIPT_FILE 2>/dev/null > /dev/null
#if exported from print use field 7
cat "$1" | egrep '^[0-9].*' | cut -d$' ' -f5 |sort -n|uniq > ip.txt
#cat "$1" | cut -d$' ' -f5 |sort -n > ip.txt

#if exported with export, use field 5
#cat "$1" | cut -d' ' -f5|sort -n > ip.txt
if [[ $LINUX -eq 1 ]]; then
	echo "#!/bin/bash" > $SCRIPT_FILE
fi
cat ip.txt | xargs -I {} echo ./check-ip.py -l $ADDRESS_LIST -i {} >> $SCRIPT_FILE
if [[ $LINUX -eq 1 ]]; then
	chmod +x $SCRIPT_FILE
fi


