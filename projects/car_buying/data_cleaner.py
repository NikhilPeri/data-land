import collections
import pandas as pd
import json
import re
import pyap

def flatten(d, parent_key='', sep='_'):
    if d is None:
        return {}

    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        new_key = re.sub(
            '([a-z0-9])([A-Z])', r'\1_\2',
            re.sub('(.)([A-Z][a-z]+)', r'\1_\2', new_key)
        ).lower()

        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def price_to_float(d):
    if 'price' in d:
        d['price'] =  float(re.sub(r'[^\d.]', '', d['price']))
    else:
        d['price'] = None

    return d

def mileage_to_int(d):
    if 'attributes_mileage_from_odometer' in d:
        d['attributes_mileage_from_odometer'] = re.sub(r'[^\d.]', '', d['attributes_mileage_from_odometer'])
        d['attributes_mileage_from_odometer'] = int(d['attributes_mileage_from_odometer']) if not d['attributes_mileage_from_odometer'] == '' else None
    else:
        d['attributes_mileage_from_odometer'] = None

    return d

def year_to_int(d):
    if 'attributes_vehicle_model_date' in d:
        d['attributes_vehicle_model_date'] = int(d['attributes_vehicle_model_date']) if not d['attributes_vehicle_model_date'] == '' else None
    return d

if __name__ == '__main__':
    import sys
    with open(sys.argv[1], 'r') as file:
        data = json.load(file)
    data = map(flatten, data)
    data = map(price_to_float, data)
    data = map(mileage_to_int, data)

    data = pd.DataFrame(data)
    data.drop_duplicates(subset='url', inplace=True)
    data.to_csv(sys.argv[2], encoding='utf-8')
