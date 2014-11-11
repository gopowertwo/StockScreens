import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates

import numpy
import time
import datetime

stocks = ['TSLA', 'GOOG']

directory = 'data/'


def graph(stock):

    try:
        filename = directory + stock + '.csv'
        date, closep, highp, lowp, openp, vol = \
            numpy.loadtxt(filename,
                          delimiter=',',
                          unpack=True,
                          converters={0: mdates.strpdate2num('%Y%m%d')})
        fig = plt.figure()

        ax1 = plt.subplot2grid((5, 1), (0, 0), rowspan=4, colspan=4)
        ax1.plot(date, openp)
        ax1.plot(date, closep)
        ax1.plot(date, lowp)
        ax1.plot(date, highp)
        plt.ylabel('Stock Price')
        ax1.grid(True)

        ax2 = plt.subplot2grid((5, 4), (4, 0), rowspan=1, colspan=4, sharex=ax1)
        ax2.bar(date, vol)
        ax2.axes.yaxis.set_ticklabels([])
        plt.ylabel('Volume')
        ax2.grid(True)

        ax1.xaxis.set_major_locator(ticker.MaxNLocator(10))
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

        ax2.xaxis.set_major_locator(ticker.MaxNLocator(10))
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

        for label in ax1.xaxis.get_ticklabels():
            label.set_rotation(45)

        for label in ax2.xaxis.get_ticklabels():
            label.set_rotation(45)

        plt.xlabel("Date")
        plt.suptitle(stock + " Stock Price")

        plt.setp(ax1.get_xticklabels(), visible=False)

        plt.subplots_adjust(left=.09, bottom=.18, right=.93, top=.94, wspace=.20, hspace=0.03)

        plt.show()

    except Exception, e:
        print(e)

graph('TSLA')
