#!python

from portfolio import portfolio
from portfolio import STOCK_FILE
from portfolio import PANDAS_DATATYPE
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from colorama import Fore
import warnings

warnings.filterwarnings('ignore')

class weekly_bull_model:
    def __init__(self):
        self.best_model = None
        self.best_mean_accuracy = None
        self.feature_set = None
        self.day_to_predict = 4
        self.this_week = None

    def prepare_data(self, symbol, TM):

        # read time series data and convert into weekly data
        data = pd.read_csv(STOCK_FILE % (symbol,TM),index_col=['Date'],parse_dates=['Date'],dtype=PANDAS_DATATYPE)
        #data = pd.read_csv(STOCK_FILE % (symbol,TM),dtype=PANDAS_DATATYPE)
        data['Date'] = data.index
        data['indexDate'] = pd.DatetimeIndex(data['Date'])
        data['weekofyear'] = data['indexDate'].dt.week
        data['dayofweek'] = data['indexDate'].dt.dayofweek

        #print(data)
        #weekly_data = data.pivot(index='weekofyear', columns='dayofweek', values=['Open','Close','High','Low','Volume'])
        weekly_data = data.pivot(index='weekofyear', columns='dayofweek', values='Open')

        # X
        weekly_data['tue_gain'] = weekly_data[1]-weekly_data[0]
        weekly_data['tue_gain'].div(weekly_data[0])

        weekly_data['wed_gain'] = weekly_data[2]-weekly_data[0]
        weekly_data['wed_gain'].div(weekly_data[0])

        weekly_data['thu_gain'] = weekly_data[2]-weekly_data[0]
        weekly_data['thu_gain'].div(weekly_data[0])

        # Y
        weekly_data['bull'] = np.where(weekly_data[self.day_to_predict] > weekly_data[0], 1, 0)
        #print(weekly_data)
        #print(self.feature_set)

        self.this_week = weekly_data[self.feature_set].tail(1)
        weekly_data = weekly_data.dropna(axis=0, how='any', subset=[0,1,2,3,4])

        #print(weekly_data)
        #print(weekly_data['bull'].values)
        #print(weekly_data[['bull']])
        
        # Apply logistic regression to predict weekend based on sunday monday
        #feature_set = ['tue_gain']
        self.feature_data = weekly_data[self.feature_set].values
        #print(feature_data)
        self.bull_data = weekly_data['bull'].values.reshape(-1,1)

    def select_feature(self, day_of_week):

        #print('Today',day_of_week)
        all_features = [0,'tue_gain','wed_gain','thu_gain']
        self.day_to_predict = 4

        if 0 == day_of_week or day_of_week > 4:
            day_of_week = 4
        else:
            self.day_to_predict = min(4,day_of_week)

        self.feature_set = {all_features[i] for i in range(self.day_to_predict)}

    def make_model(self):
        for i in range(0,10):
            weekly_train,weekly_test,bull_train,bull_test = train_test_split(self.feature_data,self.bull_data, test_size=0.33,random_state=i)
            model = LogisticRegression(random_state=i)
            model.fit(weekly_train, bull_train)
            mean_accuracy = model.score(weekly_test, bull_test)

            if self.best_model is None or self.best_mean_accuracy < mean_accuracy:
                self.best_model = model
                self.best_mean_accuracy = mean_accuracy

    def is_this_week_bull(self):
        return self.best_model.predict(self.this_week)[-1] == 1


class portfolio_intel:
    def __init__(self,port):
        self.port = port

    def bullweek(self, symbol, use_local_data=False, TM='3mo'):
        '''
        Predict if it is bull week or bear week.

        '''
        
        if not use_local_data:
            self.port.pull_helper(symbol)

        week = weekly_bull_model()
        
        day_of_week = datetime.today().weekday()
        # TODO check if the data for today is available

        week.select_feature(day_of_week)
        week.prepare_data(symbol, TM)
        week.make_model()

        #print('mean_accuracy:{mean_accuracy}'.format(mean_accuracy=week.best_mean_accuracy))

        speculation = week.is_this_week_bull()
        #print('speculation:', speculation)

        bull_speculation = 'bear'
        color = Fore.RED
        if speculation:
            bull_speculation = 'bull'
            color = Fore.GREEN


        print("{color}{company}\t\t|{day_of_week}\t\t|{mean_accuracy:.2f}\t\t|{feature_set}{speculation}".format(color=color,company=symbol,day_of_week=day_of_week,mean_accuracy=week.best_mean_accuracy,speculation=bull_speculation,feature_set=week.feature_set))

        return speculation

if __name__ == "__main__":
    tool = portfolio("./portfolio.csv")
    #tool.pull()
    print("-----")

