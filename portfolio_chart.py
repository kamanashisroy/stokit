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
BAR_EDGE_COLOR = "#000000"
RED_COLOR = "#ff000000"
GREEN_COLOR = "#00ff0000"
BAR_ALPHA = 0.5
POLAR_COMPARE_TM_INDEX = 1 # 3mo
POLAR_BOTTOM = 1.0

class chart:

    def __init__(self,port):
        self.port = port


    def status(self, display_method):
        '''
        Show the summary of shares in pie/box form
        '''

        result = self.port.status()

        if type(display_method) == str:
            display_method = [display_method]

        fig = plt.figure()

        if 'pie' in display_method:

            ax = fig.add_subplot(len(display_method), 1, display_method.index('pie')+1)
            ax.set_title('Summary %s' % self.port.title())
            ax.axis('equal')
            #ax['pie'].pie(value_list, labels=symbol_list, autopct='%1.1f%%')
            weights,texts,autotexts = ax.pie(result.VALUE, labels=result.SYMBOL, autopct='%1.1f%%')

        if 'doughnut' in display_method:

            ax = fig.add_subplot(len(display_method), 1, display_method.index('doughnut')+1)
            ax.set_title('Summary doughnut %s' % self.port.title())
            cmap = plt.get_cmap('RdYlGn')

            # convert gain_ratio to colormap
            gain_color = cmap([0.5 + x/2 for x in result.GAIN_RATIO])
            ax.pie(result.VALUE, labels=result.SYMBOL, colors=gain_color, autopct='%1.1f%%', radius=1, wedgeprops=dict(width=DOUGHNUT_SIZE, edgecolor='w'))
            #ax_doughnut.pie(value_list, colors=gain_color, radius=1-DOUGHNUT_SIZE, wedgeprops=dict(width=DOUGHNUT_SIZE, edgecolor='w'))

        if 'polar' in display_method:

            ax = fig.add_subplot(len(display_method), 1, display_method.index('polar')+1, projection='polar')
            ax.set_title('Status polar %s' % self.port.title())
            symbol_label = [r'{symbol} gain:{gain_ratio:2.2f}% $\sigma$:{sigma:2.2f}'.format(symbol=x,gain_ratio=result.GAIN_RATIO[i]*100,sigma=result.STD[i]) for i,x in enumerate(result.SYMBOL)]

            self.draw_gain_sigma_bar(ax, result.GAIN_RATIO, result.STD, symbol_label)
            #plt.ylabel('daily gain')
            #plt.xlabel('sigma')

        if 'bar' in display_method:

            ax = fig.add_subplot(len(display_method), 1, display_method.index('bar')+1)
            ax.set_title('Summary bar %s' % self.port.title())
            cmap = plt.get_cmap('RdYlGn')

            # convert gain_ratio to colormap
            gain_color = cmap([0.5 + x/2 for x in result.GAIN_RATIO])
            change_color = [RED_COLOR if x < 0 else GREEN_COLOR for x in result.GAIN_RATIO]
            
            #x_offset = range(0,len(result.SYMBOL))
            x_offset = np.cumsum([x+4 for x in result.STD])
            np.subtract(x_offset,result.STD[0])
            
            ax.bar(x_offset, height=result.COST, width=result.STD, color=gain_color, tick_label=result.SYMBOL, edgecolor=BAR_EDGE_COLOR)
            ax.bar(x_offset, height=result.GAIN, width=result.STD, color=change_color, edgecolor=BAR_EDGE_COLOR, alpha=BAR_ALPHA)
            plt.ylabel('cost and gain')
            plt.xlabel('sigma')

        plt.show()

    def compare(self, display_method):

        result  = self.port.compare()

        if type(display_method) == str:
            display_method = [display_method]

        fig = plt.figure()

        if 'table' in display_method:
            cmap = plt.get_cmap('RdYlGn')
            n_rows = len(result.PERIOD_LIST)
            n_cols = len(result.SYMBOL_LIST)
            #y_offset = np.zeros(n_cols)
            x_offset = np.arange(n_cols)
            ax = fig.add_subplot(len(display_method), 1, display_method.index('table')+1)
            for row in range(n_rows):
                #plt.bar(range(0,n_cols), height=gain_list[row], bottom=y_offset, color=colors[row], tick_label=symbol_list)
                gain_color = cmap([0.5 + x/2 for x in result.GAIN_RATIO_LIST_BY_PERIOD[row]])
                #plt.bar(x_offset/n_rows, height=gain_list[row], bottom=y_offset, color=gain_color, tick_label=symbol_list)
                ax.bar(x_offset, height=result.GAIN_RATIO_LIST_BY_PERIOD[row], width=BAR_SIZE/n_rows, color=gain_color, edgecolor=BAR_EDGE_COLOR, tick_label=result.SYMBOL_LIST)
                #y_offset = y_offset + gain_list[row]
                x_offset = x_offset + BAR_SIZE/n_rows# + width/n_rows
            #plt.table(cellText=gain_ratio_list, rowLevels=time_list, rowColours=colors, colLevels=symbol_list)
            #plt.table(cellText=gain_ratio_list, rowLevels=time_list, colLevels=symbol_list)

        #if 'candlestick' == display_method:
        #
        #    n_cols = len(result.SYMBOL_LIST)
        #    ax = np.arange(n_cols)
        #    for idx,tm in enumerate(result.PERIOD_LIST):
        #        candlestick2_ohlc(ax, result.OPEN_LIST_BY_PERIOD[idx], result.HIGH_LIST_BY_PERIOD[idx], result.HIGH_LIST_BY_PERIOD[idx], result.CLOSE_LIST_BY_PERIOD[idx])

        if 'polar' in display_method:

            ax = fig.add_subplot(len(display_method), 1, display_method.index('polar')+1, projection='polar')
            ax.set_title('Compare polar %s' % self.port.title())
            symbol_label = [r'{symbol}: gain {gain_ratio:2.2f}% $\sigma$ {sigma:2.2f}'.format(symbol=x,gain_ratio=result.GAIN_RATIO_LIST_BY_PERIOD[-1][i]*100, sigma=result.STD_LIST_BY_PERIOD[-3][i]) for i,x in enumerate(result.SYMBOL_LIST)]

            self.draw_gain_sigma_bar(ax, result.GAIN_RATIO_LIST_BY_PERIOD[-1], result.STD_LIST_BY_PERIOD[-3], symbol_label)

        if 'bar' in display_method:

            ax = fig.add_subplot(len(display_method), 1, display_method.index('bar')+1)
            ax.set_title('Compare bar %s' % self.port.title())

            symbol_label = [r'{symbol}: gain {gain_ratio:2.2f}% $\sigma$ {sigma:2.2f}'.format(symbol=x,gain_ratio=result.GAIN_RATIO_LIST_BY_PERIOD[-1][i]*100, sigma=result.STD_LIST_BY_PERIOD[-3][i]) for i,x in enumerate(result.SYMBOL_LIST)]

            self.draw_gain_sigma_bar(ax, result.GAIN_RATIO_LIST_BY_PERIOD[-1], result.STD_LIST_BY_PERIOD[-3], symbol_label, symbol_label)

            plt.ylabel('gain pct')
            plt.xlabel('sigma')

        plt.show()


    def quote(self, symbol, use_local_data, tm='3mo', display_method = 'candlestick'):
        result = self.port.quote(symbol, use_local_data)

        if 'candlestick' == display_method:
            data = pd.read_csv(result[tm],index_col=0,parse_dates=True)
            #mpf.plot(data,type='candle',mav=(3,6,9),volume=True,show_nontrading=True)
            #mpf.plot(data,type='candle',mav=(3,6,9),volume=True,show_nontrading=False)
            mpf.plot(data,type='candle',mav=(2),volume=True,show_nontrading=False)

    def draw_gain_sigma_bar(self, ax, gain_ratio, sigma, display_label, display_text=[]):
        '''
        Draw a sigma bar

        It is supposed to be a polar . But it is also possible to draw it in straight line.

        Legend is based on the edge color.

        '''
        cmap = plt.get_cmap('RdYlGn')
        gain_color = cmap([0.5 + x/2 for x in gain_ratio])

        #edge_cmap = plt.get_cmap('Dark2')
        #edge_color = edge_cmap(range(len(sigma)))
        
        radii_gain = [100*x+10 for x in gain_ratio]
        max_radii = np.max(radii_gain)

        volatility = np.sum(sigma)
        polar_volatility = (2*np.pi)/volatility

        theta_width = [x*polar_volatility for x in sigma]

        theta_offset = np.cumsum([x for x in theta_width])
        np.subtract(theta_width,sigma[0])

        ax.bar(theta_offset, radii_gain, bottom=POLAR_BOTTOM, width=theta_width, color=gain_color, edgecolor=BAR_EDGE_COLOR, alpha=BAR_ALPHA, tick_label=display_label, label=display_label)

        if display_text:
            for i, xtext in enumerate(display_text):
                ax.text(theta_offset[i], max_radii, xtext)

        #plt.legend(loc="upper left")

