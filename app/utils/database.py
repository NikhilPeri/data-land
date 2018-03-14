import sqlite3
import psycopg2

import os

class Database(object):
    def __init__(self, env=None):
        if env == None and 'APP_ENV' in os.environ:
            self.env = os.environ['APP_ENV']
        else:
            self.env = env

        if self.env == 'PRODUCTION':
            self.db = psycopg2.connect(os.environ['DATABASE_URL'])
        elif self.env == 'DEVELOPMENT':
            self.db = sqlite3.connect('../../data/development_db.sqlite')
        elif self.env == 'TEST':
            self.db = sqlite3.connect('../../data/test_db.sqlite')
        else:
            raise "Invalid APP_ENV:" + self.env

    def cursor(self):
        return self.db.cursor()
