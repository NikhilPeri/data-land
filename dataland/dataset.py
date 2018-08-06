import os
import pandas as pd

def get_template(dataset_path):
    return pd.DataFrame(columns=pd.read_csv(dataset_path, nrows=1).columns)
