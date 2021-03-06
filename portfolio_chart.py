#!python

from portfolio import portfolio
from portfolio_intel import portfolio_intel
import matplotlib.pyplot as plt
import mplfinance as mpf
from mplfinance.original_flavor import candlestick2_ohlc
import matplotlib.cm as cm
import matplotlib.colors as mplcolors
import numpy as np
import pandas as pd
from colorama import Fore

DOUGHNUT_SIZE = 0.3
POLAR_SIZE = 0.3
BAR_SIZE = 0.3
BAR_EDGE_COLOR = "#000000"
RED_COLOR = "#ff000000"
GREEN_COLOR = "#00ff0000"
BAR_ALPHA = 0.5
POLAR_COMPARE_TM_INDEX = 1 # 3mo
POLAR_BOTTOM = 10
COLOR_NORM = mplcolors.Normalize(vmin=-1,vmax=+1)

class chart:

    def __init__(self,port):
        self.port = port
        self.intel = portfolio_intel(port)


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
            gain_color = cmap([COLOR_NORM(x) for x in result.GAIN_RATIO])
            ax.pie(result.VALUE, labels=result.SYMBOL, colors=gain_color, autopct='%1.1f%%', radius=1, wedgeprops=dict(width=DOUGHNUT_SIZE, edgecolor='w'))
            #ax_doughnut.pie(value_list, colors=gain_color, radius=1-DOUGHNUT_SIZE, wedgeprops=dict(width=DOUGHNUT_SIZE, edgecolor='w'))

        if 'polar' in display_method:

            ax = fig.add_subplot(len(display_method), 1, display_method.index('polar')+1, projection='polar')
            ax.set_title('Status polar %s' % self.port.title())
            gain_label = [r'{symbol} gain:{gain_ratio:2.2f}%'.format(symbol=x,gain_ratio=result.GAIN_RATIO[i]*100) for i,x in enumerate(result.SYMBOL)]

            self.draw_gain_sigma_bar(ax, result.GAIN_RATIO, [BAR_SIZE]*len(result.SYMBOL), gain_label)

        if 'sigmapolar' in display_method:

            ax = fig.add_subplot(len(display_method), 1, display_method.index('sigmapolar')+1, projection='polar')
            ax.set_title('Status sigmapolar %s' % self.port.title())

            sigma_gain_label = [r'{symbol} gain:{gain_ratio:2.2f}% $\sigma$:{sigma:2.2f}'.format(symbol=x,gain_ratio=result.GAIN_RATIO[i]*100,sigma=result.STD[i]) for i,x in enumerate(result.SYMBOL)]
            self.draw_gain_sigma_bar(ax, result.GAIN_RATIO, result.STD, sigma_gain_label)

        if 'costpolar' in display_method:

            ax = fig.add_subplot(len(display_method), 1, display_method.index('costpolar')+1, projection='polar')
            ax.set_title('Status costpolar %s' % self.port.title())

            cost_gain_label = [r'{symbol} gain:{gain_ratio:2.2f}% cost:{cost:2.2f}'.format(symbol=x,gain_ratio=result.GAIN_RATIO[i]*100,cost=result.COST[i]) for i,x in enumerate(result.SYMBOL)]
            self.draw_gain_sigma_bar(ax, result.GAIN_RATIO, result.COST, cost_gain_label)


        if 'bar' in display_method:

            ax = fig.add_subplot(len(display_method), 1, display_method.index('bar')+1)
            ax.set_title('Summary bar %s' % self.port.title())

            self.draw_cost_gain_bar(ax, result.GAIN_RATIO, result.COST, result.GAIN, result.SYMBOL, [BAR_SIZE]*len(result.SYMBOL))
            
            plt.ylabel('cost and gain')

        if 'sigmabar' in display_method:

            ax = fig.add_subplot(len(display_method), 1, display_method.index('sigmabar')+1)
            ax.set_title('Summary sigmabar %s' % self.port.title())

            self.draw_cost_gain_bar(ax, result.GAIN_RATIO, result.COST, result.GAIN, result.SYMBOL, result.STD)
            
            plt.ylabel('cost and gain')
            plt.xlabel('sigma')

        plt.show()

    def compare(self, display_method):

        result  = self.port.compare()

        if type(display_method) == str:
            display_method = [display_method]

        fig = plt.figure()
        n_cols = len(result.SYMBOL_LIST)

        if 'heat' in display_method:
            '''
            Reference https://matplotlib.org/stable/gallery/images_contours_and_fields/image_annotated_heatmap.html
            '''
            cmap = plt.get_cmap('RdYlGn')
            n_rows = len(result.PERIOD_LIST)
            ax = fig.add_subplot(len(display_method), 1, display_method.index('heat')+1)
            ax.set_xlabel('Symbol')
            ax.set_ylabel('Change')
            ax.set_xticks(np.arange(0,n_cols,1))
            #ax.set_xticklabels(['-'] + result.SYMBOL_LIST,rotation=90,visible=True)
            ax.set_xticklabels(result.SYMBOL_LIST)
            ax.set_yticks(np.arange(n_rows))
            ax.set_yticklabels(result.PERIOD_LIST)
            for row in range(n_rows):
                for col in range(n_cols):
                    #ax.text(col, row, '{gain_ratio:2.2f}%'.format(gain_ratio=result.GAIN_RATIO_LIST_BY_PERIOD[row][col]*100), ha='center', va='center',bbox=dict(boxstyle='round', facecolor='white', edgecolor='0.3'))
                    ax.text(col, row, '{gain_ratio:2.2f}%'.format(gain_ratio=result.GAIN_RATIO_LIST_BY_PERIOD[row][col]*100), ha='center', va='center')
                
            plt.setp(ax.get_xticklabels(), rotation=45, ha="right",rotation_mode="anchor")

            #heatmap = ax.matshow(result.GAIN_RATIO_LIST_BY_PERIOD,vmin=-1,vmax=1, cmap=cmap)
            heatmap = ax.imshow(result.GAIN_RATIO_LIST_BY_PERIOD,vmin=-1,vmax=1, cmap=cmap)
            #heatmap = ax.pcolor(result.GAIN_RATIO_LIST_BY_PERIOD, cmap=cmap, edgecolors='k', linewidths=2)
            cbar = plt.colorbar(heatmap)

        if 'table' in display_method:
            cmap = plt.get_cmap('RdYlGn')
            n_rows = len(result.PERIOD_LIST)
            #y_offset = np.zeros(n_cols)
            x_offset = np.arange(n_cols)
            ax = fig.add_subplot(len(display_method), 1, display_method.index('table')+1)
            for row in range(n_rows):
                #plt.bar(range(0,n_cols), height=gain_list[row], bottom=y_offset, color=colors[row], tick_label=symbol_list)
                #gain_color = cmap([0.5 + x/2 for x in result.GAIN_RATIO_LIST_BY_PERIOD[row]])
                gain_color = cmap([COLOR_NORM(x) for x in result.GAIN_RATIO_LIST_BY_PERIOD[row]])
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
        gain_color = cmap([COLOR_NORM(x) for x in gain_ratio])

        #edge_cmap = plt.get_cmap('Dark2')
        #edge_color = edge_cmap(range(len(sigma)))
        
        radii_gain = [100*x for x in gain_ratio]
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


    def draw_cost_gain_bar(self, ax, gain_ratio, cost, gain, display_label, bar_width):
        '''
        Draw cost gain bar

        '''
        cmap = plt.get_cmap('RdYlGn')

        # convert gain_ratio to colormap
        gain_color = cmap([COLOR_NORM(x) for x in gain_ratio])
        change_color = [RED_COLOR if x < 0 else GREEN_COLOR for x in gain_ratio]
        
        x_dist = np.max(bar_width)/2
        x_offset = np.cumsum([x+x_dist for x in bar_width])
        x_offset = np.subtract(x_offset, bar_width)

        ax.bar(x_offset, height=cost, width=bar_width, color=gain_color, tick_label=display_label, edgecolor=BAR_EDGE_COLOR, alpha=BAR_ALPHA)
        ax.bar(x_offset, height=gain, width=bar_width, color=change_color, edgecolor=BAR_EDGE_COLOR, alpha=BAR_ALPHA)

    def bullweek(self, symbol, use_local_data=False, TM='3mo'):
        '''
        Predict if it is bull week or bear week.

        '''
        if 'all' == symbol:
            result  = self.port.compare()
            print('symbol\t\t|week day\t|accuracy\t|speculation')
            print(' ---\t\t| ---\t\t| ---\t\t| ---')
            for cur_symbol in result.SYMBOL_LIST:
                self.intel.bullweek(cur_symbol, True, TM)
        else:
            self.intel.bullweek(symbol, use_local_data, TM)

        print(Fore.RESET)

