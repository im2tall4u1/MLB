#!/bin/bash
# Convert JSON-ish DNS domain files to CSV - david.switzer@mlb.com

INPUT=$1
OUTPUT="$INPUT.csv"
IFS=$'\n'

# Check if a real file was given on the command line
if test -f "$INPUT"; then

# header
#grep "A" internal_dns_example.txt |egrep -v -e '(CNAME|SRV|AAAA)' | perl -ne "s/\[AGE:\d*\]\W\d{3,4}// && print"
# if $1 = A, hostname = blank

echo "host,ip,FQDN,asn,asnOrgName" > "$OUTPUT"

#DOMAIN=$(grep "D(" "$INPUT" | cut -d \' -f 2)
DOMAIN=$(grep Database $INPUT | awk {'print $6'})

for HOSTLINE in $(grep "A" "$INPUT" | grep "A" | egrep -i -v -e '(SRV|CNAME|SOA|AAAA)'  |perl -ne "s/\[AGE:\d*\]\W\d{3,4}// && print" | perl -ne "s/\s+/ / && print" | perl -ne "s/\t/ / && print" | perl -ne "s/\r// && print"); do
	HOST=$(echo "$HOSTLINE" | awk {'print $1'})
	IP=$(echo "$HOSTLINE" | awk {'print $3'})
	FQDN="$HOST.$DOMAIN"
        # change "fqdn" to just domain name for the "@" hostname, if it exists
        if [ "$HOST" = "@" ]; then FQDN="$DOMAIN"; fi
	#
	# if host is A.. that means the hostname was blank; rearrange how we grab IP
	if [ "$HOST" = "A" ]; then
		HOST=""
		IP=$(echo "$HOSTLINE" | awk {'print $2'})
	fi


	ASNINFO=$(whois -h whois.cymru.com "$IP" | grep -v "AS Name")
	ASN=$(echo "$ASNINFO" | awk {'print $1'})
	ASNORG=$(echo "$ASNINFO" | cut -d \| -f 3 | sed -e "s/^[ \t]*//" -e "s/,//g")

	# rearrange these as needed - don't forget to rearrange header above
	echo "$HOST,$IP,$FQDN,$ASN,$ASNORG" >> "$OUTPUT"
done 

echo "Done - output file: $OUTPUT"

else echo "You need to supply an input file name on command line!"; fi
