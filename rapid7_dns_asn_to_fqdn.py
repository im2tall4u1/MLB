#!/usr/bin/env python3

from __future__ import print_function
import rapid7vmconsole
import base64
import logging
import sys
import pandas as pd
import os
from glob import glob

######### Program Start ###########

n = input("Enter the site ids you would like to update: ")
user_input_list = list(map(int, n.split()))
for i in user_input_list:
    site_id = i

files = ['rapid7_dns_asn_good.csv', 'rapid7_dns_asn_ignore.csv']
input_file = []

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            input_file.append(os.path.join(root, name))
    print(input_file)
            #print(os.path.join(root, name))

for i in files:
    find(i, '/Users')

good_asn_numbers = input_file[0]
ignored_asn_numbers = input_file[1]
result = [y for x in os.walk('/Users/trent.williams/Desktop/rapid7_dnscontrol_sync/mlb_gitclonerepo') for y in glob(os.path.join(x[0], '*.csv'))]
fqdn = []



def mass_compare(master_sheet):
    ######### Variable and file setup ###########
    # csv_master_sheet = master_sheet # Main CSV that known ASN numbers are compared to [Will change]
    #site_id = site_id_number

    ######## File comparison ############

    good_numbers_list = []
    bad_numbers_list = []

    good_and_bad_numbers = [] # numbers in doc 1 and doc 2
    def file_comparison():
        """
        This function combines good_asn_numbers and bad_asn_numbers and puts them into a list.
        :return: List with good/bad asn numbers to later be used for comparison.
        """
        good_numbers = open(good_asn_numbers, 'r', encoding='utf-8-sig')  # File with good ASN numbers
        bad_numbers = open(ignored_asn_numbers, 'r', encoding='utf-8-sig') # File with undesired ASN numbers



        for i in good_numbers:
            good_and_bad_numbers.append(i.rstrip('\n'))
            good_numbers_list.append(i.rstrip('\n'))

        for r in bad_numbers:
            good_and_bad_numbers.append(r.strip('\n'))
            bad_numbers_list.append(r.strip('\n'))

        #print(good_and_bad_numbers)
    file_comparison()



######### Identifies common ASN numbers between known good/undesired csv and main csv file #########
    df = pd.read_csv(master_sheet, error_bad_lines=False, header=None)
    csv_master_sheet_numbers = list(set(df[3].tolist()))
    common_values = []
    nonmatching_values = []
    def common_numbers(a, b):
        """
        This function compares ASN numbers between documents and identifies matching numbers between them. Will alert if
        there are no matches.
        :param a: Type - List: Master CSV sheet numbers.
        :param b: Type - List: Numbers in good/bad asn documents.
        :return: Common values in both lists OR no common element alert.
        """
        for element in a:
            if element in b:
                common_values.append(element)
            else:
                nonmatching_values.append(element)
        print(common_values)
    common_numbers(csv_master_sheet_numbers, good_numbers_list)
######### ASN to FQDN ############

    df = df[df[3].isin(common_values)]
    wanted_fqdn_data = list(df[2])
    #print(wanted_fqdn_data)
    #print(len(wanted_fqdn_data))
    for data in wanted_fqdn_data:
        fqdn.append(data)
for y in result:
    mass_compare(y)


print(fqdn)

######### Identifies common ASN numbers between known good/undesired csv and main csv file #########

common_values = []
nonmatching_values = []
def common_numbers(a, b):
    """
    This function compares ASN numbers between documents and identifies matching numbers between them. Will alert if
    there are no matches.
    :param a: Type - List: Master CSV sheet numbers.
    :param b: Type - List: Numbers in good/bad asn documents.
    :return: Common values in both lists OR no common element alert.
    """
    for element in a:
        if element in b:
            common_values.append(element)
        else:
            nonmatching_values.append(element)
    #print(common_values)
    # print(nonmatching_values)


common_numbers(csv_master_sheet_numbers, good_and_bad_numbers)
#print(common_values)

######### ASN to FQDN ############

#df = df[df[3].isin(common_values)]
#wanted_fqdn_data = list(df[2])
#print(len(wanted_fqdn_data))
#print(wanted_fqdn_data)
