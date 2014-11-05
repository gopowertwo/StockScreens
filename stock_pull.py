#!/usr/bin/python2.7

try:
    import urllib.request as urllib2
except:
    import urllib2

import time
import csv
import os

stocks = ['GOOG', 'AAPL', 'MSFT', 'AMZN', 'EBAY', 'TSLA']
directory = 'data/'

url = 'http://chartapi.finance.yahoo.com/instrument/1.0/%s/chartdata;type=quote;range=%s/csv/'


def pull_data(stock):
    try:
        fileline = directory + stock + '.csv'
        print(fileline)
        url_stock = url % (stock, '5d')

        source = urllib2.urlopen(url_stock)
        cr = list(csv.reader(source))

        save_file = open(fileline, 'w')  # TODO: Change to 'a'

        for row in cr[1:]:
            if len(row) == 6 and 'values' not in row[0]:
                line = ','.join(row) + '\n'
                save_file.write(line)

        print('Pulled', stock)
        print('Sleeping...')
        time.sleep(1)

    except Exception, e:
        print('Problem!', e)


def main():

    if not os.path.exists(directory):
        os.makedirs(directory)

    for company in stocks:
        print('Pulling', company)
        pull_data(company)

main()
