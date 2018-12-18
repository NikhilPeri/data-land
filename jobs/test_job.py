from dataland.scheduler import Job, schedule

job = Job(
    sched=schedule.every(1).minute,
    operations=[]
)

if __name__ == '__main__':
    job.run()
