import sys
import pandas as pd
import os
import glob
import csv


home = os.getcwd() ## Current working directory from which script operates

print("The current working directory is: %s" % home)

desired_files = ['rapid7_dns_0_asn_good.csv', 'rapid7_dns_0_asn_ignore.csv'] ## Necessary files
input_file = []

os.chdir('..')
file_location = os.path.abspath(os.curdir)
file_in = './'


print('Checking for necessary files in directory: %s ' % file_location)

## find function walks computer to look for files necessary files

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            input_file.append(os.path.join(root, name))

for i in desired_files:
    find(i, file_location)

## If files are not found, program will exit.

if len(input_file) == 2:
    print("Necesssary files found...")
else:
    sys.exit("Necessary files not found. Verify that they are on your computer.")

good_asn_numbers = input_file[0] # Known good asn numbers
ignored_asn_numbers = input_file[1] # asn numbers to be ignored

## get_csv_files grabs every csv file from the documents_asn_converted directory.
## places all files and their paths in empty list (result).

result = []
def get_csv_files():
    os.chdir(os.getcwd() + '/documents_asn_converted' )
    print("Retrieving csv files from: %s" % os.getcwd())
    print("current working directory is: %s" % os.getcwd())
    csv_files = glob.glob('*.csv')
    for elem in csv_files:
        result.append(str(os.getcwd()) + '/' + elem)
get_csv_files()




old_dir = os.chdir(home) ## changes working directory back to starting directory.


print("Checking if asn numbers in good and ignored documents are shared...")

def shared_asn_function():
    """
    This function combines good_asn_numbers and bad_asn_numbers and puts them into a list.
    :return: List with good/bad asn numbers to later be used for comparison.
    """
    good_numbers = open(good_asn_numbers, 'r', encoding='utf-8-sig')  ## File with good ASN numbers
    bad_numbers = open(ignored_asn_numbers, 'r', encoding='utf-8-sig') ## File with undesired ASN numbers
    errored_asn_numbers = []

    good_numbers_list = []
    bad_numbers_list = []

    for i in good_numbers:
        good_numbers_list.append(i.rstrip('\n'))

    for r in bad_numbers:
        bad_numbers_list.append(r.strip('\n'))

    matching_good_ignore = [x for x in good_numbers_list if x in bad_numbers_list]
    if len(matching_good_ignore) >= 1:
        for elem in matching_good_ignore:
            errored_asn_numbers.append(elem)
        myset = set(errored_asn_numbers)
        print("Shared ASN numbers are: " + str(myset))
        sys.exit("ASN numbers cannot be shared. Check data.")
    else:
        print("No shared ASN numbers... continuing process...")
shared_asn_function()


## update directories to new structure
## are you deleting these directories first - or does python handle it - what happens when you run it 3x
## if directory exists are you deleting or cleaning it up first at least?

os.chdir('..')
print("Creating new directories in: %s" % os.getcwd())

manual_review_directory = ('rapid7_dns_manual_review_documents')
good_asn_directory = ('rapid7_dns_good_asn_documents')
ignored_asn_directory = ('rapid7_dns_ignored_asn_documents')

def create_manual_review_directory():
    """
    This function creates a new directory for files manual review files. Directory will not be created if it already exists.
    :return: confirmation that new directory was created OR that a directory exists.
    """
    try:
        os.mkdir(manual_review_directory)
        print('Manual review directory created.')
    except:
        pass
        #print('Manual review directory already exists.')
create_manual_review_directory()

def create_good_asn_directory():
    """
    This function creates a new directory for good asn files. Directory will not be created if it already exists.
    :return: confirmation that new directory was created OR that a directory exists.
    """
    try:
        os.mkdir(good_asn_directory)
        print('Good asn directory created.')
    except:
        pass
        #print('Good asn directory already exists.')
create_good_asn_directory()

def create_ignored_asn_directory():
    """
    This function creates a new directory for ignored asn files. Directory will not be created if it already exists.
    :return: confirmation that new directory was created OR that a directory exists.
    """
    try:
        os.mkdir(ignored_asn_directory)
        print('Ignored asn directory created.')
    except:
        pass
        #print('Ignored asn directory already exists.')
create_ignored_asn_directory()

print("Directories created...")



######################### REOPEN FILES ##########################
"""
files must be reopened to be used again
"""
reopen_desired_files = ['rapid7_dns_0_asn_good.csv', 'rapid7_dns_0_asn_ignore.csv']
reopen_input_file = []

## note the documents_asn_clonedgit is now where all *.csv live
## I think it's actually in documents_asn_converted
print('Reopening necessary files...')
def reopen_files(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            reopen_input_file.append(os.path.join(root, name))

for i in reopen_desired_files:
    reopen_files(i, file_location)


reopened_good_asn_numbers = reopen_input_file[0] # Known good asn numbers
reopened_ignored_asn_numbers = reopen_input_file[1] # asn numbers to be ignored

print("Necessary files reopened...")
######################################################################

print("Creating documents...")


good_numbers_list = []
bad_numbers_list = []

## These lists are used to compare contents of the csv files. 

good_and_bad_numbers = [] # numbers in doc 1 and doc 2

## Uses pandas dataframe to enable comment support in csv files.

good_numbers = pd.read_csv(reopened_good_asn_numbers, header=None)  # File with good ASN numbers
bad_numbers = pd.read_csv(reopened_ignored_asn_numbers, header=None) # File with undesired ASN numbers

doc_one_list = good_numbers[0].tolist()
doc_two_list = bad_numbers[0].tolist()

errored_asn_numbers = []


for i in doc_one_list:
    good_and_bad_numbers.append(str(i))
    good_numbers_list.append(str(i))

for r in doc_two_list:
    good_and_bad_numbers.append(str(r))
    bad_numbers_list.append(str(r))




    ################ Creation of Manual Review Files #################
def init_manual_review_file_creation(master_sheet):
    csv_master_sheet = master_sheet # Main CSV that known ASN numbers are compared to [Will change]
    df = pd.read_csv(master_sheet, index_col=None, warn_bad_lines=False, error_bad_lines=False, quoting=csv.QUOTE_NONE, header=None)
    numbers_not_present =[]
    def manual_review_file_creation():
        base = os.path.basename(master_sheet)
        os.path.splitext(base)
        manual_review_file_base = os.path.splitext(base)[0]
        csv_master_sheet_numbers = list(set(df[3].tolist())) # Numbers from the CSV that is the point of comparison
        manual_review_numbers = list(set(df[3].tolist()) - set(good_and_bad_numbers)) # numbers not on good/bad asn document but on csv master sheet
        df.loc[df[3].isin(manual_review_numbers)].to_csv(manual_review_directory + '/' + manual_review_file_base + '_manual_review.csv', index=False, header=None)
    manual_review_file_creation()
for i in result:
    init_manual_review_file_creation(i)
print("Manual review files created...")


    ################ Good ASN CSV Files ##################
def init_good_file_creation(master_sheet):
    base = os.path.basename(master_sheet)
    os.path.splitext(base)
    csv_master_sheet = master_sheet # Main CSV that known ASN numbers are compared to [Will change]
    header = ['host', 'ip', 'FQDN', 'asn', 'asnOrgName']
    df = pd.read_csv(master_sheet, index_col=None, warn_bad_lines=False, error_bad_lines=False, quoting=csv.QUOTE_NONE, header=None)
    numbers_not_present =[]
    def good_file_creation():
        good_asn_file_base = os.path.splitext(base)[0]
        df.loc[df[3].isin(good_numbers_list)].to_csv(good_asn_directory + '/' + good_asn_file_base + '_good_asn.csv', index=False, header=header)
    good_file_creation()
for i in result:
    init_good_file_creation(i)
print("Good ASN number files created...")



    ################ Ignored ASN CSV Files ################
def init_ignored_file_creation(master_sheet):
    base = os.path.basename(master_sheet)
    os.path.splitext(base)
    csv_master_sheet = master_sheet # Main CSV that known ASN numbers are compared to [Will change]
    header = ['host', 'ip', 'FQDN', 'asn', 'asnOrgName']
    df = pd.read_csv(master_sheet, index_col=None, warn_bad_lines=False, error_bad_lines=False, quoting=csv.QUOTE_NONE, header=None)
    numbers_not_present =[]
    def ignored_file_creation():
        ignored_asn_file_base = os.path.splitext(base)[0]
        ignored_review_numbers = list(set(df[3].tolist()) - set(good_numbers_list)) # numbers on ignored asn doc and master sheet
        df.loc[df[3].isin(bad_numbers_list)].to_csv(ignored_asn_directory + '/' + ignored_asn_file_base + '_ignored_asn.csv', index=False, header=header)
    ignored_file_creation()
for i in result:
    init_ignored_file_creation(i)

print("Ignored ASN number files created...")

print('Process complete. Check working directory for good/ignored/manual review asn number documents.')
