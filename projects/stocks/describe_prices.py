import logging
import pandas as pd

from dataland.scheduler import UpdateOperation

class DescribePrices(UpdateOperation):
    INPUT = 'data/stocks/snp_500_list.csv'

    def update(self, stock_list):
        for index, company in stock_list.iterrows():
            prices = pd.read_csv('data/stocks/prices/{}.csv'.format(company['Symbol']))
            stock_list.at[index, 'price_count'] = len(prices)

            intraday = pd.Series(prices['high'] - prices['low'])[:365].describe()
            stock_list.at[index, 'intraday_mean'] = intraday['mean']
            stock_list.at[index, 'intraday_stddev'] = intraday['std']

        logging.info('Processes {} stock symbols'.format(len(stock_list)))
        return stock_list

if __name__ == '__main__':
    DescribePrices().perform()
