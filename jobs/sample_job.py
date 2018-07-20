import logging

class SampleJob(object):
    def run(self):
        logging.warn('yoo')

job = SampleJob()
