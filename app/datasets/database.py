from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os

class Database(object):
    @classmethod
    def get_engine(cls):
        if os.environ.has_key('DATALAND_PRODUCTION'):
            return create_engine(os.environ['DATABASE_URL'])
        else:
            return create_engine('postgresql://nikhilperi:password@localhost:5432/dataland_dev')

    @classmethod
    def get_session(cls):
        engine = Database.get_engine()
        Session = sessionmaker(bind=engine)
        return Session()
