#!/bin/bash
echo "Installing Rapid7 Python API Client Dependency"
rm -rf file_rapid7_python_api_client
mkdir -p file_rapid7_python_api_client
git clone https://github.com/rapid7/vm-console-client-python.git file_rapid7_python_api_client
pip3 install pandas
