import os
import sys
import signal
import logging
import schedule
import importlib

from time import sleep
from dataland.utils import timestamp

JOB_BLACKLIST=[
    '__init__.py'
]

class Job(object):
    def __init__(self, sched=[], operations=[]):
        self.module = self.__module__
        self.operations = operations
        if type(sched) is schedule.Job:
            sched = [sched]
        for s in sched:
            s.do(self.run)

    def run(self):
        try:
            logging.info('Job running {}'.format(self.module))
            for operation in self.operations:
                operation.perform()
            logging.info('Job succedded {}'.format(self.module))
        except Exception as e:
            logging.error('Job failed {}'.format(self.module))

def configure_logging():
    formatter = logging.Formatter(
        fmt='[%(levelname)s] %(asctime)s.%(msecs)03d | %(message)s',
        datefmt='%Y-%m-%d %I:%M:%-S'
    )

    file_stream = logging.StreamHandler(stream=open(
        os.path.join('logs', '{}.log'.format(timestamp())),
        mode='a+'
    ))
    file_stream.setFormatter(formatter)
    file_stream.setLevel(20)

    console_stream = logging.StreamHandler(stream=sys.stdout)
    console_stream.setFormatter(formatter)
    console_stream.setLevel(30)

    logging.getLogger().setLevel(20)
    logging.getLogger().addHandler(file_stream)
    logging.getLogger().addHandler(console_stream)

def load_jobs():
    for parent_dir, _, files in os.walk(os.path.join(os.getcwd(), 'jobs')):
        for file in files:
            if not file.endswith('.py') or file in JOB_BLACKLIST:
                continue
            module_name = (
                os.path.join(os.path.relpath(parent_dir), file)
                .replace('.py', '')
                .replace('/', '.')
            )
            try:
                importlib.import_module(module_name).job.module = module_name
                logging.info('Job loaded {}'.format(module_name))
            except Exception as e:
                logging.error('Failed to load Job {}'.format(module_name))
                raise e

if __name__ == '__main__':
    configure_logging()
    load_jobs()

    logging.info('Starting scheduler')

    def signal_handler(sig, frame):
        global active
        active = False

    signal.signal(signal.SIGINT, signal_handler)
    active = True
    while active:
        schedule.run_pending()
        sleep(1)

    logging.info('Stopping scheduler')
