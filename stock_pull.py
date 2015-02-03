#!/usr/bin/python2.7

try:
    import urllib.request as urllib2
except:
    import urllib2

import time
import csv
import os
import sys
import sqlite3

from datetime import datetime

directory = 'data/'

url = 'http://chartapi.finance.yahoo.com/instrument/1.0/%s/chartdata;type=quote;range=%s/csv/'


def init_db(db_name):
        """
            Connect to database and create the necessary tables if they don't exist
        """

        conn = sqlite3.connect(db_name)
        cur = conn.cursor()

        # Ugly but quick way to apply simple changes to the tables
        # cur.execute('''DROP TABLE tDayStock''')
        # cur.execute('''DROP TABLE tMinuteStock''')
        # conn.commit()

        # Create tables if they don't exist
        cur.execute('''CREATE TABLE IF NOT EXISTS tDayStock (ticker TEXT, datestamp TEXT,
                        high REAL, low REAL, open REAL, close REAL, volume REAL, PRIMARY KEY (ticker, datestamp))''')
        cur.execute('''CREATE TABLE IF NOT EXISTS tMinuteStock (ticker TEXT, datestamp TEXT,
                        high REAL, low REAL, open REAL, close REAL, volume REAL, PRIMARY KEY (ticker, datestamp))''')
        return conn


def get_data_yahoo_year(stock):
    try:
        print(str(time.strftime('%Y-%m-%d %H:%M:%S')))
        print('Pulling: ' + stock)

        filename = directory + stock + '.csv'
        url_stock = url % (stock, '1y')

        source = urllib2.urlopen(url_stock)
        cr = list(csv.reader(source))

        cur = database.cursor()
        cur.execute('SELECT * FROM tDayStock')
        data = cur.fetchone()

        data = list()
        for row in cr:
            if len(row) == 6 and 'values' not in row[0]:
                # if int(row[0]) > int(last):
                row.insert(0, stock)
                data.append(tuple(row))

        cur.executemany('''INSERT INTO tDayStock(ticker, datestamp, high, low, open, close, volume)
                        VALUES(?, ?, ?, ?, ?, ?, ?)''', data)

        return 0

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
        time.sleep(0)

    except Exception, e:
        print('Problem: %s' % e)


def main():

    if not os.path.exists(directory):
        os.makedirs(directory)

    while True:
        for company in const._stocks:
            get_data_yahoo_year(company)
        break

    database.commit()
    database.close()

if __name__ == '__main__':
    database = init_db('finance_data.db')
    main()
