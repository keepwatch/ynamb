# YNAMB
YNAB (You Need a Budget) is a popular tool for managing income, expenses, and budgets. Mint is a popular tool for collecting transaction information from bank and credit card websites. YNAMB (You Need a Minty Budget) enables YNAB users to easily import Mint data!

## Syntax
    usage: ynambImportProcessor.py [-h] [-if IMPORTFILE] [-ld LASTDATE]
    
    Converts Mint CSV transactions into YNAB CSV import files, one for each
    account.
    
    optional arguments:
      -h, --help            show this help message and exit
      -if IMPORTFILE, --importFile IMPORTFILE
                            Optional: Define the full path to the Mint CSV import
                            file. Default is the most recent transactions*.csv
                            file in current directory.
      -ld LASTDATE, --lastDate LASTDATE
                            Optional: Define a date (in mm/dd/YYYY format) before
                            which all transactions are ignored. Default is
                            01/01/1900.

## Usage Instructions

1. Install the appropriate version of Python (2.7.9+)
2. Download the Python script and place it in a directory.
3. [Download your Mint transactions](https://mint.lc.intuit.com/questions/950809-how-do-i-export-transactions) as a single CSV file and save it in the same directory as the Python script
4. Run the script using the syntax above.
5. Take the output files that result (one per Mint account) and [import them into the appropriate YNAB account](http://www.youneedabudget.com/support/article/how-to-import-transactions).

### Account Mapping Feature
Since Mint and YNAB account names could be vastly different, the script supports an account mapping feature. To enable, 
create a CSV file containing the following lines (where CHECKING is the Mint account name and "Personal Checking" is the YNAB account name):

    Mint,YNAB
    CHECKING,Personal Checking

If the file does not exist or doesn't contain a Mint account name for a given account, the files are written with the Mint account name as the prefix.
