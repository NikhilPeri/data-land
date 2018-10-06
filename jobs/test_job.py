import logging

from dataland.scheduler import schedule, Job

class TestOperation(object):
    def perform(self):
        logging.error('run')

job = Job(
    sched=schedule.every(1).minute,
    operations=[TestOperation()]
)
