#!/bin/bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
echo "Installing Required Python Libraries"
git clone https://github.com/rapid7/vm-console-client-python.git file_rapid7_python_api_client
pip3 install selenium
pip3 install beautifulsoup4
pip3 install pandas
brew install geckodriver
