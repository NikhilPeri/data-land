from dataland.scheduler import Job

from projects.proline.scrapers import ScrapeOdds, ScrapeResults
from projects.proline.model import Train, Predict

job = Job(
    sched=schedule.every(1).day.at('09:00'),
    operations=[
        ScrapeOdds(),
        ScrapeResults(),
        Predict()
    ]
)
