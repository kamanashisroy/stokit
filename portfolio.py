#!python

import yfinance as yf
import csv
from collections import namedtuple

COMPANY = namedtuple("COMPANY","SYMBOL,COUNT,COST")

STOCK_FILE = ".stock/history_%s_%s.csv"
TIME_PROFILE = ['1y', '3mo', '1mo', '5d', '1d']

COMPARE_RESULT = namedtuple("COMPARE_RESULT", "SYMBOL_LIST,PERIOD_LIST,PRICE_LIST_BY_PERIOD,GAIN_LIST_BY_PERIOD,GAIN_RATIO_LIST_BY_PERIOD,OPEN_LIST_BY_PERIOD,HIGH_LIST_BY_PERIOD,LOW_LIST_BY_PERIOD,CLOSE_LIST_BY_PERIOD")

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
        print('symbol\t\t|    cost\t\t|   value\t\t|    gain\t\t|gain pct')
        print(' ---\t\t| ---    \t\t| ---    \t\t| ---    \t\t| ---')
        total_value = 0.0
        for company in self.companies:
            with open(STOCK_FILE % (company.SYMBOL,TIME_PROFILE[-1]), 'r') as fstatus:
                reader = csv.DictReader(fstatus)
                last = None
                for x in reader:
                    last = x
                #print(x)
                current_value = company.COUNT*float(last['Close'])
                value_list.append(current_value)
                gain_list.append(current_value-company.COST)
                gain_ratio = 0
                if company.COST != 0:
                    gain_ratio = (current_value-company.COST)/company.COST
                gain_ratio_list.append(gain_ratio)
                print("{company}\t\t|{cost:8.2f}\t\t|{value:8.2f}\t\t|{gain:8.2f}\t\t|{gain_pct:8.2f}".format(company=company.SYMBOL,cost=company.COST,value=current_value,gain=(current_value-company.COST),gain_pct=gain_ratio*100))
                total_value += current_value

        print("Total total_investment", total_investment)
        print("Total value", total_value)
        print("gain/loss", total_value-total_investment)

        return symbol_list, cost_list, value_list, gain_list, gain_ratio_list

    def compare(self):

        price_list_timely = []
        gain_list_timely = []
        gain_ratio_list_timely = []
        ohlc_open_list_timely = []
        ohlc_high_list_timely = []
        ohlc_low_list_timely = []
        ohlc_close_list_timely = []

        for tm in TIME_PROFILE:
            price_list = []
            gain_list = []
            gain_ratio_list = []
            ohlc_open_list = []
            ohlc_high_list = []
            ohlc_low_list = []
            ohlc_close_list = []
            print(tm)
            print("-----------------------")
            print('symbol\t\t|last\t\t|today\t\t|gain\t\t|gain pct')
            print(' ---\t\t| ---\t\t| ---\t\t| ---\t\t| ---')
            for company in self.companies:
                with open(STOCK_FILE % (company.SYMBOL,tm), 'r') as fstatus:
                    reader = csv.DictReader(fstatus)
                    last = None
                    first = None
                    xopen,xhigh,xlow,xclose = 0.0,0.0,0.0,0.0
                    xhigh = 0
                    xlow = 0
                    xclose = 0

                    for x in reader:
                        last = x
                        if first is None:
                            first = x
                            try:
                                xopen,xhigh,xlow,xclose = float(x['Open']),float(x['High']),float(x['Low']),float(x['Close'])
                            except:
                                print("Value error")
                                first = None
                                continue
                        xlow = min(xlow,float(x['Low']))
                        xhigh = max(xhigh,float(x['High']))
                            
                    ohlc_open_list.append(xopen)
                    ohlc_high_list.append(xhigh)
                    ohlc_low_list.append(xlow)
                    ohlc_close_list.append(xclose)

                    current_value = float(last['Low'])
                    price_list.append(current_value)

                    prev_value = float(first['Open'])
                    gain_list.append(current_value-prev_value)

                    gain_ratio = 0
                    if prev_value != 0:
                        gain_ratio = (current_value-prev_value)/prev_value
                    gain_ratio_list.append(gain_ratio)

                    print("{company}\t\t|{prev:.2f}\t\t|{current:.2f}\t\t|{gain:.2f}\t\t|{gain_pct:.2f}%".format(company=company.SYMBOL,prev=prev_value,current=current_value,gain=(current_value-prev_value),gain_pct=gain_ratio*100))
            price_list_timely.append(price_list)
            gain_list_timely.append(gain_list)
            gain_ratio_list_timely.append(gain_ratio_list)
            ohlc_open_list_timely.append(ohlc_open_list)
            ohlc_high_list_timely.append(ohlc_high_list)
            ohlc_low_list_timely.append(ohlc_low_list)
            ohlc_close_list_timely.append(ohlc_close_list)
            print()

        return COMPARE_RESULT([company.SYMBOL for company in self.companies],TIME_PROFILE,price_list_timely,gain_list_timely,gain_ratio_list_timely,ohlc_open_list_timely,ohlc_high_list_timely,ohlc_low_list,ohlc_close_list_timely)

 
    def quote(self, symbol, pullit=True):

        if pullit:
            self.pull_helper(symbol)

        # TODO dump today's information

        result = {tm:(STOCK_FILE % (symbol,tm)) for tm in TIME_PROFILE}
        return result

if __name__ == "__main__":
    tool = portfolio("./portfolio.csv")
    tool.dump()
    #tool.pull()
    print("-----")

