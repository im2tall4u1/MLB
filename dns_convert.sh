#!/bin/bash
# Convert JSON-ish DNS domain files to CSV - david.switzer@mlb.com / trent.williams@mlb.com

INPUT=$1
OUTPUT="$INPUT.csv"
IFS=$'\n'

# Check if a real file was given on the command line
if test -f "$INPUT"; then

# header
echo "host,ip,FQDN,asn,asnOrgName" > "$OUTPUT"

DOMAIN=$(grep "D(" "$INPUT" | cut -d \' -f 2)

## ignore examples like   //A('securemlbextrabases.cname', '209.102.213.73', TTL(60)),
## json commments should not end up in final CSV

## restore/retain original column names

for HOSTLINE in $(grep "A(" "$INPUT"); do
	HOST=$(echo "$HOSTLINE" | awk {'print $1'} | sed -e "s/\'//g" -e "s/A(//g" -e "s/,//g")
	IP=$(echo "$HOSTLINE" | awk {'print $2'} | sed -e "s/\'//g" -e "s/A(//g" -e "s/,//g")
	FQDN="$HOST.$DOMAIN"
	ASNINFO=$(whois -h whois.cymru.com "$IP" | grep -v "AS Name")

	## if none found it's likely internal?
	## RFC1918

	ASN=$(echo "$ASNINFO" | awk {'print $1'})
	## ZZ Internal Range RFC1918
	ASNORG=$(echo "$ASNINFO" | cut -d \| -f 3 | sed -e "s/^[ \t]*//" -e "s/,//g")
	# change "fqdn" to just domain name for the "@" hostname, if it exists
	if [ "$HOST" = "@" ]; then FQDN="$DOMAIN"; fi
	# rearrange these as needed - don't forget to rearrange header above
	echo "$HOST,$IP,$FQDN,$ASN,$ASNORG" >> "$OUTPUT"
done

echo "Done - output file: $OUTPUT"

else echo "You need to supply an input file name on command line!"; fi
