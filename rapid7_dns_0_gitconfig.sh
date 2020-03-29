#In order to run the script, you must store your credentials in Git.
echo "You must have Github Enterprise assigned via https://mlb.okta.com/"
echo "You must have read permissions for the repository https://github.mlbam.net/Infrastructure/dnscontrol-conf"
echo "You must have set up via your Settings > Developer Settings > Personal Access Tokens https://github.mlbam.net/settings/tokens"
echo "Select Repo and User Scopes only!! Take note of your username!!"
git config --global credential.helper store
rm -rf documents_asn_clonedgit
mkdir -p documents_asn_clonedgit
git clone https://github.mlbam.net/Infrastructure/dnscontrol-conf.git documents_asn_clonedgit
