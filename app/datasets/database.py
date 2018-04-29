from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os

class Database(object):
    @classmethod
    def get_engine(cls, enviroment):
        if enviroment == 'production':
            return create_engine(os.environ['DATABASE_URL'])
        elif enviroment == 'test':
            return create_engine('sqlite:///tmp/test.db')

    @classmethod
    def get_session(cls, enviroment):
        engine = Database.get_engine(enviroment)
        Session = sessionmaker(bind=engine)
        return Session()
