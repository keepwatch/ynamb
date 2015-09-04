import os
import csv
import sys
import glob
import argparse
import datetime

# Read cli options (argparse) / set default options
parsedMappings = {'Date': 'Date', 'Description': 'Payee', 'Original Description': 'Memo'}
todayString = datetime.datetime.today().strftime('%Y%m%d-%H%M%S')
ynabFieldnames = ['Date', 'Payee', 'Category', 'Memo', 'Outflow', 'Inflow']
accountMappings = {}

def arguments():
    '''Parses command line arguments and sets defaults.'''
    parser = argparse.ArgumentParser(description='Converts Mint CSV transactions into YNAB CSV import files, one for each account.')
    parser.add_argument('-if', '--importFile', default=max(glob.iglob('transactions*.csv'), key=os.path.getctime), 
        help='Optional: Define the full path to the Mint CSV import file. Default is the most recent transactions*.csv file in current directory.')
    parser.add_argument('-ld', '--lastDate', default='01/01/1900',
        help='Optional: Define a date (in %m/%d/%Y format) before which all transactions are ignored. Default is 01/01/1900.')
    return parser.parse_args()

args = arguments()

lastDate = datetime.datetime.strptime(args.lastDate, '%m/%d/%Y')

# Read an accounts mapping file
if os.path.isfile('accountMappings.csv'):
    with open('accountMappings.csv', 'r') as csvMapReadObject:
        mapReader = csv.DictReader(csvMapReadObject)
        for mapLine in mapReader:
            accountMappings[mapLine['Mint']] = mapLine['YNAB']
else:
    accountMappings = {}

# Read the transactions file
tempEntryList = []
print 'Using Mint CSV file {}'.format(os.path.abspath(args.importFile))
with open(args.importFile, 'r') as csvReadObject:
    reader = csv.DictReader(csvReadObject)

    # Process the transactions file, assigning items to a new temp list
    for line in reader:
        tempEntryList.append(line)

# Read items from the temp list
accountDict = {}

for entry in tempEntryList:
    # ignore transactions before lastDate
    if entry['Date'][1] == '/':
        tempDate1 = '0' + entry['Date']
    else:
        tempDate1 = entry['Date']

    if tempDate1[4] == '/':
        tempDate2 = tempDate1[:3] + '0' + tempDate1[3:]
    else:
        tempDate2 = tempDate1

    if datetime.datetime.strptime(tempDate2, '%m/%d/%Y') > lastDate:

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
                    print 'New transaction type observed - exiting.'
                    sys.exit(0)

        # add tempDict to appropriate account in accountDict
        if entry['Account Name'] in accountMappings:
            accountName = accountMappings[entry['Account Name']]
        else:
            accountName = entry['Account Name']

        if accountName not in accountDict:
            accountDict[accountName] = [tempDict]
        else:
            accountDict[accountName].append(tempDict)

# Write the account lists (for account in accountList)
for account in accountDict:
    with open('{}_{}.csv'.format(todayString, account), 'w') as csvWriteObject:
        csvDictWriter = csv.DictWriter(csvWriteObject, fieldnames=ynabFieldnames)

        csvDictWriter.writeheader()

        for transaction in accountDict[account]:
            csvDictWriter.writerow(transaction)
