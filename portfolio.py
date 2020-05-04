#!python

import yfinance as yf
import csv
from collections import namedtuple

COMPANY = namedtuple("COMPANY","SYMBOL,COUNT,COST")

STOCK_FILE = ".stock/history_%s.csv"

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

    def pull(self):
        '''
        Pull data from yfinance
        '''
        for x in self.companies:
            print("pulling ", x)
            f = open(STOCK_FILE % x.SYMBOL, 'w')
            ticker = yf.Ticker(x.SYMBOL)
            df = ticker.history(period='3m')
            f.write(df.to_csv())
            f.close()
            
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
        total_value = 0.0
        for company in self.companies:
            with open(STOCK_FILE % company.SYMBOL, 'r') as fstatus:
                reader = csv.DictReader(fstatus)
                last = None
                for x in reader:
                    last = x
                #print(x)
                current_value = company.COUNT*float(x['Close'])
                value_list.append(current_value)
                gain_list.append(current_value-company.COST)
                gain_ratio = 0
                if company.COST != 0:
                    gain_ratio = (current_value-company.COST)/company.COST
                gain_ratio_list.append(gain_ratio)
                print("{company}\t\t|{cost:.2f}\t\t|{value:.2f}\t\t|{gain:.2f}".format(company=company.SYMBOL,cost=company.COST,value=current_value,gain=(current_value-company.COST)))
                total_value += current_value

        print("Total total_investment", total_investment)
        print("Total value", total_value)
        print("gain/loss", total_value-total_investment)

        return symbol_list, cost_list, value_list, gain_list, gain_ratio_list


if __name__ == "__main__":
    tool = portfolio("./portfolio.csv")
    tool.dump()
    #tool.pull()
    print("-----")

