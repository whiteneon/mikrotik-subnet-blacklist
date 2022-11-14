#!/bin/bash

#SCRIPT_FILE="newip.sh"
SCRIPT_FILE="newip.ps1"

ADDRESS_LIST="Blacklist"

rm ip.txt 2>/dev/null > /dev/null
#rm newip.ps1 2>/dev/null > /dev/null
rm $SCRIPT_FILE 2>/dev/null > /dev/null
#if exported from print use field 7
cat "$1" | cut -d$' ' -f5 |sort -n > ip.txt

#if exported with export, use field 5
#cat "$1" | cut -d' ' -f5|sort -n > ip.txt
#echo "#!/bin/bash" > $SCRIPT_FILE
cat ip.txt | xargs -I {} echo ./check-ip.py -l $ADDRESS_LIST -i {} >> $SCRIPT_FILE
#chmod +x $SCRIPT_FILE


