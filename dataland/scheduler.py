import os
import sys
import yaml
import logging
import importlib

from datetime import timedelta, datetime, time
from dataland.file_utils import lastest_file, timestamped_file

DATETIME_FORMAT = '%Y-%m-%d-%H%M'
FREQUENCY_MAPINGS = {
    '1h':     timedelta(hours=1),
    '4h':     timedelta(hours=4),
    '8h':     timedelta(hours=8),
    '12h':    timedelta(hours=12),
    'daily':  timedelta(days=1),
    'weekly': timedelta(days=7),
}

SUCCESS_STATUS = 'SUCCESS'
FAILURE_STATUS = 'FAILED'

class Job(object):
    def run(self):
        raise NotImplemented

class Scheduler(object):
    def __init__(self, schedule_file='config/schedule.yml', log_dir='logs'):
        self.log_dir = log_dir

        self._load_schedule(schedule_file)
        self._load_schedule_history()

    def run(self):
        pending_jobs = self._pending_jobs()
        if len(pending_jobs) == 0:
            return

        self._configure_logging()
        for name, job in pending_jobs.items():
            try:
                module = importlib.import_module(job['module'])
                logging.info('Scheduler running {}'.format(job['module']))
                module.job.run()
            except Exception as e:
                self._mark_job_failure(name)
                logging.error('Scheduler failed {}'.format(job['module']))
                logging.error(e.message)

            self._mark_job_sucess(name)
            logging.info('Scheduler succedded {}'.format(job['module']))

        self._save_schedule_history()
        logging.shutdown()


    def _load_schedule(self, file):
        with open(file, 'r') as schedule:
            self.schedule = yaml.load(schedule)

    def _load_schedule_history(self):
        self.history = {}
        for job_name in self.schedule.keys():
            self.history[job_name] = {
                'last_run': '0001-01-01-0000',
                'status': None
            }

        with lastest_file(os.path.join(self.log_dir, 'history'), type='yml', mode='r') as schedule_history:
            history = yaml.load(schedule_history)
            if history != None:
                self.history.update(history)

    def _save_schedule_history(self):
        with timestamped_file(os.path.join(self.log_dir, 'history'), type='yml', mode='w+') as schedule_file:
            schedule_file.write(yaml.dump(self.history, default_flow_style=False))

    def _pending_jobs(self):
        jobs = {}
        for name, job in self.schedule.items():
            if job.has_key('after') and datetime.now().time() < datetime.strptime(job['after'], '%H:%M').time():
                continue
            if job.has_key('before') and datetime.now().time() > datetime.strptime(job['before'], '%H:%M').time():
                continue

            next_run = datetime.strptime(self.history[name]['last_run'], DATETIME_FORMAT) + FREQUENCY_MAPINGS[job['frequency']]
            if datetime.now() > next_run or self.history[name]['status'] != SUCCESS_STATUS:
                jobs[name] = job
        logging.info('Scheduler has {} pending job(s)'.format(len(jobs)))
        return jobs

    def _mark_job_sucess(self, job_name):
        self.history[job_name]['last_run'] = datetime.strftime(datetime.now(), DATETIME_FORMAT)
        self.history[job_name]['status'] = SUCCESS_STATUS

    def _mark_job_failure(self, job_name):
        self.history[job_name]['last_run'] = datetime.strftime(datetime.now(), DATETIME_FORMAT)
        self.history[job_name]['status'] = FAILURE_STATUS

    def _configure_logging(self):
        formatter = logging.Formatter(
            fmt='[%(levelname)s] %(asctime)s.%(msecs)03d | %(message)s',
            datefmt='%Y-%m-%d %I:%M:%-S'
        )
        file_stream = logging.StreamHandler(stream=timestamped_file(os.path.join(self.log_dir, 'scheduler'), type='log', mode='a+'))
        file_stream.setFormatter(formatter)
        file_stream.setLevel(20)
        console_stream = logging.StreamHandler(stream=sys.stdout)
        console_stream.setFormatter(formatter)
        console_stream.setLevel(30)

        logging.getLogger().addHandler(file_stream)
        logging.getLogger().addHandler(console_stream)

if __name__ == '__main__':
    Scheduler().run()
