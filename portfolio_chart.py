#!python

from portfolio import portfolio
import matplotlib.pyplot as plt
import mplfinance as mpf
from mplfinance.original_flavor import candlestick2_ohlc
import matplotlib.cm as cm
import numpy as np
import pandas as pd

DOUGHNUT_SIZE = 0.3
POLAR_SIZE = 0.3
BAR_SIZE = 0.3
class chart:

    def __init__(self,port):
        self.port = port


    def status(self, display_method):
        '''
        Show the summary of shares in pie/box form
        '''

        symbol_list, cost_list, value_list, gain_list, gain_ratio_list = self.port.status()

        #print("Showing [%s]" % display_method)

        if 'pie' == display_method:

            fig,ax_basic = plt.subplots()
            ax_basic.set_title('Summary %s' % self.port.title())
            ax_basic.axis('equal')
            #ax1.pie(value_list, labels=symbol_list, autopct='%1.1f%%')
            weights,texts,autotexts = ax_basic.pie(value_list, labels=symbol_list, autopct='%1.1f%%')

        elif 'doughnut' == display_method:

            fig,ax_doughnut = plt.subplots()
            ax_doughnut.set_title('Summary doughnut %s' % self.port.title())
            cmap = plt.get_cmap('RdYlGn')

            # convert gain_ratio to colormap
            gain_color = cmap([0.5 + x/2 for x in gain_ratio_list])
            ax_doughnut.pie(value_list, labels=symbol_list, colors=gain_color, autopct='%1.1f%%', radius=1, wedgeprops=dict(width=DOUGHNUT_SIZE, edgecolor='w'))
            #ax_doughnut.pie(value_list, colors=gain_color, radius=1-DOUGHNUT_SIZE, wedgeprops=dict(width=DOUGHNUT_SIZE, edgecolor='w'))

        elif 'polar' == display_method:

            fig,ax_polar = plt.subplots(111, projection='polar')
            ax_polar.set_title('Summary polar %s' % self.port.title())
            cmap = plt.get_cmap('RdYlGn')

            gain_color = cmap([0.5 + x/2 for x in gain_ratio_list])
            total_value = 0
            for x in value_list:
                total_value += x

            radii = [10*x/total_value for x in value_list]

            #ax_polar.bar(gain_ratio_list, radii, width=POLAR_SIZE, bottom=0.0, color=gain_color, alpha=0.5, labels=symbol_list)
            ax_polar.bar(gain_ratio_list, radii, width=POLAR_SIZE, bottom=0.0, color=gain_color, alpha=0.5)
        
        elif 'bar' == display_method:

            fig,ax_doughnut = plt.subplots()
            ax_doughnut.set_title('Summary bar %s' % self.port.title())
            cmap = plt.get_cmap('RdYlGn')

            # convert gain_ratio to colormap
            gain_color = cmap([0.5 + x/2 for x in gain_ratio_list])
            ax_doughnut.bar(range(0,len(symbol_list)), height=cost_list, color=gain_color, tick_label=symbol_list)
            ax_doughnut.bar(range(0,len(symbol_list)), height=gain_list)

        plt.show()

    def compare(self, display_method):

        result  = self.port.compare()

        if 'table' == display_method:
            cmap = plt.get_cmap('RdYlGn')
            n_rows = len(result.PERIOD_LIST)
            n_cols = len(result.SYMBOL_LIST)
            #y_offset = np.zeros(n_cols)
            x_offset = np.arange(n_cols)
            for row in range(n_rows):
                #plt.bar(range(0,n_cols), height=gain_list[row], bottom=y_offset, color=colors[row], tick_label=symbol_list)
                gain_color = cmap([0.5 + x/2 for x in result.GAIN_RATIO_LIST_BY_PERIOD[row]])
                #plt.bar(x_offset/n_rows, height=gain_list[row], bottom=y_offset, color=gain_color, tick_label=symbol_list)
                plt.bar(x_offset, height=result.GAIN_RATIO_LIST_BY_PERIOD[row], width=BAR_SIZE/n_rows, color=gain_color, edgecolor='#000000', tick_label=result.SYMBOL_LIST)
                #y_offset = y_offset + gain_list[row]
                x_offset = x_offset + BAR_SIZE/n_rows# + width/n_rows
            #plt.table(cellText=gain_ratio_list, rowLevels=time_list, rowColours=colors, colLevels=symbol_list)
            #plt.table(cellText=gain_ratio_list, rowLevels=time_list, colLevels=symbol_list)

        elif 'candlestick' == display_method:

            n_cols = len(result.SYMBOL_LIST)
            ax = np.arange(n_cols)
            for idx,tm in enumerate(result.PERIOD_LIST):
                candlestick2_ohlc(ax, result.OPEN_LIST_BY_PERIOD[idx], result.HIGH_LIST_BY_PERIOD[idx], result.HIGH_LIST_BY_PERIOD[idx], result.CLOSE_LIST_BY_PERIOD[idx])

        plt.show()


    def quote(self, symbol, tm='3mo', display_method = 'candlestick'):
        result = self.port.quote(symbol)

        if 'candlestick' == display_method:
            data = pd.read_csv(result[tm],index_col=0,parse_dates=True)
            mpf.plot(data,type='candle',mav=(3,6,9),volume=True,show_nontrading=True)

