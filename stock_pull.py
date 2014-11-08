#!/usr/bin/python2.7

try:
    import urllib.request as urllib2
except:
    import urllib2

import time
import csv
import os
import sys

from datetime import datetime


stocks = ['GOOG', 'AAPL', 'MSFT', 'AMZN', 'EBAY', 'TSLA']
directory = 'data/'

url = 'http://chartapi.finance.yahoo.com/instrument/1.0/%s/chartdata;type=quote;range=%s/csv/'


def pull_data(stock):
    try:
        print(str(time.strftime('%Y-%m-%d %H:%M:%S')))
        print('Pulling: ' + stock)

        filename = directory + stock + '.csv'
        url_stock = url % (stock, '5d')

        source = urllib2.urlopen(url_stock)
        cr = list(csv.reader(source))

        try:
            with open(filename) as f:
                lines = f.readlines()
            last = lines[-1].strip('\n').split(',')[0] \
                if len(lines) > 0 else 0
        except:
            last = 0

        data = ""
        for row in cr:
            if len(row) == 6 and 'values' not in row[0]:
                if int(row[0]) > int(last):
                    data += ','.join(row) + '\n'

        with open(filename, 'a') as f:
            f.write(data.strip('\n'))

        print('Pulled: ' + stock)
        time.sleep(5)

    except Exception, e:
        print('Problem: %s' % e)


def main():

    if not os.path.exists(directory):
        os.makedirs(directory)

    while True:
        for company in stocks:
            pull_data(company)
            print('Sleeping... \n')
        time.sleep(300)

if __name__ == '__main__':
    main()
