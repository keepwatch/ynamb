import os
import csv
import sys
import glob
import argparse

# Read cli options (argparse) / set default options
parsedMappings = {'Date': 'Date', 'Description': 'Payee', 'Original Description': 'Memo'}

def arguments():
    """Parses command line arguments and sets defaults."""
    parser = argparse.ArgumentParser(description='Converts Mint CSV transactions into YNAB CSV import files, one for each account.')
    parser.add_argument('-if', '--importFile', default=max(glob.iglob('transactions*.csv'), key=os.path.getctime), 
        help='Optional: Define the full path to the Mint CSV import file. Default is the most recent transactions*.csv file in current directory.')
    return parser.parse_args()

args = arguments()

print "Using Mint CSV file {}".format(os.path.abspath(args.importFile))

# Read the transactions file
tempEntryList = []
with open(args.importFile, 'r') as csvReadObject:
    reader = csv.DictReader(csvReadObject)

    # Process the transactions file, assigning items to a new temp list
    for line in reader:
        tempEntryList.append(line)

# Read items from the temp list and pop them if they should be added to an account list (for item in tempList)
accountDict = {}

for entry in tempEntryList:
    # parse Mint CSV format into YNAB CSV format
    tempDict = {}
    for detailItem in entry:
        if detailItem in parsedMappings:
            tempDict[parsedMappings[detailItem]] = entry[detailItem]
        elif detailItem == 'Amount':
            if entry['Transaction Type'] == 'debit':
                tempDict['Outflow'] = entry['Amount']
                tempDict['Inflow'] = 0
            elif entry['Transaction Type'] == 'credit':
                tempDict['Inflow'] = entry['Amount']
                tempDict['Outflow'] = 0
            else:
                print "New transaction type observed - exiting."
                sys.exit(0)

    # add tempDict to appropriate account in accountDict
    if entry['Account Name'] not in accountDict:
        accountDict[entry['Account Name']] = [tempDict]
    else:
        accountDict[entry['Account Name']].append(tempDict)

# Write the account lists (for account in accountList)
