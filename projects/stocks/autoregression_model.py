import pandas as pd

WINDOW_SIZE=30

class BuildTrainingSet(TransformOperation):

    INPUT = 'data/stocks/snp_500_list.csv'
    OUTPUT = 'data/stocks/autoregression_model/train.csv'

    NUMBER_OF_STOCKS_TO_SAMPLE = 30

    def transform(self, stock_list):
        stock_list = stock_list.sample(NUMBER_OF_STOCKS_TO_SAMPLE)
        train_set = pd.DataFrame(columns=[''])
        for index, company in stock_list.iterrows():
            prices = pd.read_csv('data/stocks/prices/{}.csv'.format(company['Symbol']))
