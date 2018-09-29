from google.cloud import storage

global bucket
bucket = storage.Client()


def remove_client():
    client = None

def get_client():
    return client
