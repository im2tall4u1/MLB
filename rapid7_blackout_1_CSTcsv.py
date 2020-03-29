import csv
import os
import pandas as pd

INPUT_FILE = input("Specify the CSV to be modified. Include file extension: ")
OUTPUT_FILE = input("Specify name of finished CSV file. Include file extension: ")

file_in = './'
input_file = []


def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            input_file.append(os.path.join(root, name))


find(INPUT_FILE, file_in)
print(input_file)

new_file = input_file.pop(0)

df = pd.read_csv(new_file)
#print(df)

newdf = df.drop(df.columns[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]], axis=1)
newdf2 = newdf.drop([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], axis=0)

print(newdf2)
newdf2.to_csv(OUTPUT_FILE, header=None, index=False)

newcsv = os.getcwd() + '/' + OUTPUT_FILE

finalstring = []
with open(newcsv, "r") as file:
    for i in file:
        addedstring = (i.rstrip() +',9,00,17')
        finalstring.append(addedstring.replace('20,', '2020,'))
with open(newcsv, "w") as file:
    file.write('\n'.join(finalstring))


