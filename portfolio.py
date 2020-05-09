#!python

import yfinance as yf
import csv
import math
import pandas as pd
import numpy as np
from collections import namedtuple
from colorama import Fore


STOCK_FILE = ".stock/history_%s_%s.csv"
TIME_PROFILE = ['1y', '3mo', '1mo', '5d', '1d']
PANDAS_DATATYPE = {'High':np.float64, 'Low': np.float64, 'Close': np.float64, 'Volume': np.float64, 'Dividends': np.float64, 'Stock Splits': np.float64}

COMPANY = namedtuple("COMPANY","SYMBOL,COUNT,COST")
COMPARE_RESULT = namedtuple("COMPARE_RESULT", "SYMBOL_LIST,COST_LIST,PERIOD_LIST,STD_LIST_BY_PERIOD,GAIN_LIST_BY_PERIOD,GAIN_RATIO_LIST_BY_PERIOD,OPEN_LIST_BY_PERIOD,HIGH_LIST_BY_PERIOD,LOW_LIST_BY_PERIOD,CLOSE_LIST_BY_PERIOD")
STATUS_RESULT = namedtuple("STATUS_RESULT", "SYMBOL,COST,VALUE,STD,GAIN,GAIN_RATIO")

class portfolio:
    def __init__(self, filename):
        self.companies = []
        for row in csv.reader(open(filename, 'r'), delimiter='|', skipinitialspace=True):
            symbol = row[0].strip()
            count = int(row[1].strip())
            cost = float(row[2].strip())
            self.companies.append(COMPANY(symbol,count,cost))
        self.filename = filename

    def title(self):
        return self.filename

    def show(self):
        for company in self.companies:
            print(company)

    def pull_helper(self, symbol):
        for tm in TIME_PROFILE:
            f = open(STOCK_FILE % (symbol,tm), 'w')
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=tm)
            f.write(df.to_csv())
            f.close()

    def pull(self):
        '''
        Pull data from yfinance
        '''
        for x in self.companies:
            print("pulling ", x)
            for tm in TIME_PROFILE:
                self.pull_helper(x.SYMBOL)
            
    def status(self):
        '''
        Show current status of the stock
        '''
        symbol_list = []
        cost_list = []
        value_list = []
        std_list = []
        gain_list = []
        gain_ratio_list = []

        ####################################
        # calculate total_investment, symbol_list, cost_list
        ####################################
        total_investment = 0.0
        for company in self.companies:
            total_investment += company.COST
            symbol_list.append(company.SYMBOL)
            cost_list.append(company.COST)

        #################################################
        # calculate total_value, value_list, gain_list, gain_ratio_list
        #################################################
        print('symbol\t\t|    sigma\t\t|    cost\t\t|   value\t\t|    gain\t\t|gain pct')
        print(' ---\t\t| ---    \t\t| ---    \t\t| ---    \t\t| ---    \t\t| ---')
        total_value = 0.0
        for company in self.companies:

            # calculate gain on daily data
            data = pd.read_csv(STOCK_FILE % (company.SYMBOL,TIME_PROFILE[-1]),dtype=PANDAS_DATATYPE)
            xopen = data['Open'].values[0]
            xclose = data['Close'].values[-1]

            # calculate standard deviation of 3 month data
            data = pd.read_csv(STOCK_FILE % (company.SYMBOL,'3mo'),index_col=0,parse_dates=True,dtype=PANDAS_DATATYPE)
            xstd = data['Close'].std()

            current_value = xclose*company.COUNT
            value_list.append(current_value)
            std_list.append(xstd)
            gain_list.append(current_value-company.COST)
            gain_ratio = 0
            if company.COST != 0:
                gain_ratio = (current_value-company.COST)/company.COST
            gain_ratio_list.append(gain_ratio)

            color = Fore.GREEN
            if gain_ratio < 0:
                color = Fore.RED

            tail = ''
            if gain_ratio < 0:
                tail = ''.join(['-']*int(math.ceil(-gain_ratio*20)))
            else:
                tail = ''.join(['+']*int(math.ceil(gain_ratio*20)))

            print("{color}{company}\t\t|{sigma:8.2f}\t\t|{cost:8.2f}\t\t|{value:8.2f}\t\t|{gain:8.2f}\t\t|{gain_pct:8.2f} \t\t{tail}".format(color=color,company=company.SYMBOL,sigma=xstd,cost=company.COST,value=current_value,gain=(current_value-company.COST),gain_pct=gain_ratio*100,tail=tail))
            total_value += current_value

        print(Fore.RESET)
        print("Total total_investment", total_investment)
        print("Total value", total_value)
        print("gain/loss", total_value-total_investment)

        return STATUS_RESULT(SYMBOL=symbol_list, COST=cost_list, VALUE=value_list, STD=std_list, GAIN=gain_list, GAIN_RATIO=gain_ratio_list)

    def compare(self):

        std_list_timely = []
        gain_list_timely = []
        gain_ratio_list_timely = []
        ohlc_open_list_timely = []
        ohlc_high_list_timely = []
        ohlc_low_list_timely = []
        ohlc_close_list_timely = []

        for tm in TIME_PROFILE:
            std_list = []
            gain_list = []
            gain_ratio_list = []
            ohlc_open_list = []
            ohlc_high_list = []
            ohlc_low_list = []
            ohlc_close_list = []
            print(tm)
            print("-----------------------")
            print('symbol\t\t|last\t\t|today\t\t|std \t\t|gain\t\t|gain pct')
            print(' ---\t\t| ---\t\t| ---\t\t| ---\t\t| ---')
            for company in self.companies:
                data = pd.read_csv(STOCK_FILE % (company.SYMBOL,tm),dtype=PANDAS_DATATYPE)
                xlow = data['Low'].min()
                xhigh = data['High'].max()
                xopen = data['Open'].values[0]
                xclose = data['Close'].values[-1]
                xstd = data['Close'].std()

                std_list.append(xstd)
                gain_list.append(xclose-xopen)
                gain_ratio = 0
                if xopen > 0:
                    gain_ratio = (xclose-xopen)/xclose
                gain_ratio_list.append(gain_ratio)

                color = Fore.GREEN
                if gain_ratio < 0:
                    color = Fore.RED

                tail = ''
                if gain_ratio < 0:
                    tail = ''.join(['-']*int(math.ceil(-gain_ratio*20)))
                else:
                    tail = ''.join(['+']*int(math.ceil(gain_ratio*20)))

                print("{color}{company}\t\t|{prev:.2f}\t\t|{current:.2f}\t\t|{std:0.2f}\t\t|{gain:.2f}\t\t|{gain_pct:.2f}% \t\t{tail}".format(color=color,company=company.SYMBOL,prev=xopen,current=xclose,std=xstd,gain=(xclose-xopen),gain_pct=gain_ratio*100,tail=tail))

            std_list_timely.append(std_list)
            gain_list_timely.append(gain_list)
            gain_ratio_list_timely.append(gain_ratio_list)
            ohlc_open_list_timely.append(ohlc_open_list)
            ohlc_high_list_timely.append(ohlc_high_list)
            ohlc_low_list_timely.append(ohlc_low_list)
            ohlc_close_list_timely.append(ohlc_close_list)
            print(Fore.RESET)

        return COMPARE_RESULT([company.SYMBOL for company in self.companies],[company.COST for company in self.companies],TIME_PROFILE,std_list_timely,gain_list_timely,gain_ratio_list_timely,ohlc_open_list_timely,ohlc_high_list_timely,ohlc_low_list,ohlc_close_list_timely)

 
    def quote(self, symbol, use_local_data=False):

        if not use_local_data:
            self.pull_helper(symbol)

        # TODO dump today's information

        result = {tm:(STOCK_FILE % (symbol,tm)) for tm in TIME_PROFILE}
        return result

if __name__ == "__main__":
    tool = portfolio("./portfolio.csv")
    tool.dump()
    #tool.pull()
    print("-----")

