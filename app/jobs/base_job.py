from app.datasets.database import Database

class BaseJob(object):
    @classmethod
    def perform(cls):
        obj = cls()
        obj.run()

    def __init__(self):
        self.db = Database.get_session()

    def run():
        raise NotImplemented

    def save_record(self, record):
        try:
            self.db.add(record)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print(e)
