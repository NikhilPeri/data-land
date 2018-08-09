import pandas as pd



class BuildTrainingSet(TransformOperation):
    INPUT = 'data/stocks/snp_500_list.csv'
    OUTPUT = 'data/stocks/autoregression_model/train.csv'

    def transform(self, stock_list):
        
    series = Series.from_csv('daily-minimum-temperatures.csv', header=0)
    values = DataFrame(series.values)
    dataframe = concat([values.shift(1), values], axis=1)
    dataframe.columns = ['t-1', 't+1']
    result = dataframe.corr()
    print(result)
