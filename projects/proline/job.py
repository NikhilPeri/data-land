from dataland.scheduler import Job

from projects.proline.scrapers import ScrapeOdds, ScrapeResults
from projects.proline.model import Train, Predict

job = Job(stages=[
    ScrapeOdds(),
    ScrapeResults(),
    Perdict()
])
