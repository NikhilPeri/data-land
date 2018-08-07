import os
from datetime import datetime

def incremental_timestamp():
    return datetime.now().strftime('%Y-%m-%d-%H%M')

def timestamped_file(dir, type='csv', mode='w+'):
    filepath = os.path.join(dir, "{}.{}".format(incremental_timestamp(), type))
    return open(filepath, mode)

def latest_subdirectory(dir):
    subdirectories = [sd for sd in os.listdir(dir) if os.path.isdir(os.path.join(dir, sd))]
    return os.path.join(dir, sorted(subdirectories)[-1])

def lastest_file(dir, type='csv', mode='r+'):
    files = [file for file in os.listdir(dir) if file.endswith(type)]
    filepath = os.path.join(dir, sorted(files)[-1])
    return open(filepath, mode)
