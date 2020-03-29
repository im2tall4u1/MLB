#!/bin/bash
echo "Converting cloned dnscontrol-conf Git Repo to CSV"
mkdir -p ./documents_asn_converted/
rm -rf ./documents_asn_converted/*
(cd ./documents_asn_clonedgit/config_root/locked_external &&
for FILE in $(find . -iname '*js'); do
	DOMAIN=$(echo $FILE | cut -d \/ -f 3)
	echo Domain: $DOMAIN -- processing $FILE
	cp -avf $FILE ../../../documents_asn_converted/$DOMAIN
	../../../file_manipulations/dns_convert.sh ../../../documents_asn_converted/$DOMAIN
	rm -rf ../../../documents_asn_converted/$DOMAIN
done)
(cd ./documents_asn_clonedgit/config_root/internal &&
for FILE in $(find . -iname '*js'); do
	DOMAIN=$(echo $FILE | cut -d \/ -f 3)
	echo Domain: $DOMAIN -- processing $FILE
	cp -avf $FILE ../../../documents_asn_converted/$DOMAIN
	../../../file_manipulations/dns_convert.sh ../../../documents_asn_converted/$DOMAIN
  rm -rf ../../../documents_asn_converted/$DOMAIN
done)
(cd ./documents_asn_clonedgit/config_root/external &&
for FILE in $(find . -iname '*js'); do
	DOMAIN=$(echo $FILE | cut -d \/ -f 3)
	echo Domain: $DOMAIN -- processing $FILE
	cp -avf $FILE ../../../documents_asn_converted/$DOMAIN
	../../../file_manipulations/dns_convert.sh ../../../documents_asn_converted/$DOMAIN
	rm -rf ../../../documents_asn_converted/$DOMAIN
done)
