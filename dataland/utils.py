import os
import sys
import logging
from datetime import datetime

def timestamp():
    return datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
