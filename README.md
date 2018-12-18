Are you shy about your _small data_? In this world of distributed file systems,
stream processing, and cluster computing you may think that the best way to do your data science
projects is to pay a bunch of money for some machines in the cloud.

But in reality you just want to run a webscraper once a day to populate a dataset with the
latest stock market prices. **Dataland is prefect for all your small data needs** and can be
run using only free tier services.

# Deployment
Dataland is designed to run on a gcloud free-tier f1 micro instance (0.6 GB ram).  
It combines the lazy evaluation of ![Dask Dataframes](http://dask.pydata.org/en/latest/dataframe.html)
and a locally cached google cloud storage bucket in order to perform operations on
larger than memory datasets.  

# Features

Dataland has 3 noteworthy tools to accelerate development:
- [Storage](dataland/storage.py), is an abstraction layer for a gcloud bucket which handles local
caching to reduce the network cost of the system.  While providing a backup of datasets
that can be accessed by a dataland scheduler or a personal laptop.

- [Jobs](dataland/operations.py), is the framework for writing pipelines to be run one a fixed schedule
in order to update and modify datasets.

- [Notification](dataland/notification.py), provides and interface for email notifications to be sent
from any job via the mailgun free tier.

## Writing a Job
There are two important concepts here:
1. **Operation** is an atomic action that can be applied to a dataframe. The two main types of operations
are the:
  - AppendOperation, which adds data to an existing dataframe
  - TransformOperation, which takes in one or many dataframe and outputs a new dataframe
2. **Job** contains a pipeline of operations which are run in order. Operations will be applied to
the state of the dataset after its previous changes are applied.

```
from dataland.scheduler import Job, schedule

job = Job(
    sched=schedule.every(1).day.at('09:00'),
    operations=[
      # Pipeline of Operations
    ]
)
```
A job can be defined as above using the following ![schedule api](https://schedule.readthedocs.io/en/stable/)
and once placed int the `jobs/` of this project will automatically be picked up and run the next time
the `dataland/schedule.py` is run (Hot reloading is in WIP)
