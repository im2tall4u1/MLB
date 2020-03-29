#!/bin/bash
echo "Cloning MLB Github Enterprise dnscontrol-conf Repo"
rm -rf documents_asn_clonedgit
mkdir -p documents_asn_clonedgit
git clone https://github.mlbam.net/Infrastructure/dnscontrol-conf.git documents_asn_clonedgit
