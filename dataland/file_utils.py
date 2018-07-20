import os
from datetime import datetime

def incremental_timestamp():
    return datetime.utcnow().strftime('%Y-%m-%d-%H%M')

def timestamped_file(dir, type='csv', mode='w+'):
    filepath = os.path.join(dir, "{}.{}".format(incremental_timestamp(), type))
    return open(filepath, mode)

def lastest_file(dir, type='csv', mode='w+'):
    files = [file for file in os.listdir(dir) if file.endswith(type)]
    if files == []:
        return timestamped_file(dir, type=type, mode=mode)
    else:
        filepath = os.path.join(dir, sorted(files)[-1])
        return open(filepath, mode)
