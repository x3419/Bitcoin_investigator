__author__ = "Alex Bernier"
__date__ = "5/20/17"
__version__ = 1.0
__description__ = "Investigates bitcoin wallet activity and exports to CSV file. Following the book \"Learning python for forensics\""

import argparse
import logging
import csv
import json
import urllib2
import sys
from datetime import datetime
import os

def main(bitcoin_address):

    logging.log(level=logging.DEBUG, msg="Fetching JSON object and parsing into a python structure")

    try:
        unparsed = urllib2.urlopen("https://blockchain.info/address/{}?format=json".format(bitcoin_address))
    except urllib2.URLError as e:
        print "Incorrect bitcoin address"
        logging.log(level=logging.DEBUG, msg="Error opening URL: " + e.reason)
        exit()

    parsed = json.load(unparsed)

    logging.log(level=logging.DEBUG, msg="Printing account & transaction info")

    csv_headers = ["Hash", "Date"]

    with open(os.getcwd() + "\\report.csv","wb") as csvfile:
        print os.getcwd() + "report.csv"
        writer = csv.writer(csvfile)
        writer.writerow(csv_headers)

        # Print current account info
        print "Current account info:\n{:=^22}".format("")
        print "Balance: {}".format(int(parsed['final_balance'])*10**-8)
        print "Total sent: {}".format(int(parsed['total_sent'])*10**-8)
        print "Total received: {}".format(int(parsed["total_received"])*10**-8)
        print "{:=^22}\n\n".format("")

        print "Transaction info:"
        # Print transaction info
        for txs_entry in parsed['txs']:
            row = []
            print "{:=^22}".format("")
            print "Hash: {}".format(txs_entry['hash'])
            row.append(txs_entry['hash'])
            print "Time: {}".format(datetime.fromtimestamp(
                int(txs_entry['time']) ).strftime('%Y-%m-%d %H:%M:%S'))
            row.append(datetime.fromtimestamp(
                int(txs_entry['time']) ).strftime('%Y-%m-%d %H:%M:%S'))

            print "{:=^22}".format("")

            for out in txs_entry['out']:
                print "Address sent: {}".format(out['addr'])
                print "Amount sent: {}".format(int(out['value']) * 10**-8)

            print "{:=^22}\n".format("")
            writer.writerow(row)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Investigates wallet activity")
    parser.add_argument("ADDRESS",help="Bitcoin address")
    args = parser.parse_args()
    logging.basicConfig(filename="activity.log",level=logging.DEBUG, format='%(asctime)s | %(levelname)s | %(message)s', filemode='w')
    logging.log(level=logging.INFO, msg="Starting bitcoin wallet investigator, version {}".format(__version__))
    logging.log(level=logging.DEBUG, msg="Windows version: {}".format(sys.getwindowsversion()))
    main(args.ADDRESS)