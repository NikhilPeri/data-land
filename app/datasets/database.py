from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os

class Database(object):
    @classmethod
    def get_session():
        engine = create_engine(os.environ['DATABASE_URL'])
        Session = sessionmaker(bind=engine)
        return Session()
