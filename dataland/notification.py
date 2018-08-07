import os
import yaml
import requests
from markdown2 import markdown

from requests.auth import HTTPBasicAuth

from dataland import get_secret, NOTIFICATION_CONFIG

MAILGUN_URL = 'https://api.mailgun.net/v3'
MAILGUN_USER = 'api'

def email_notification(topic_name, markdown_body):
    topic = None
    with open(NOTIFICATION_CONFIG, 'r') as notification_config:
        topics = yaml.load(notification_config)
        if not topics.has_key(topic_name):
            raise ValueError("Could find topic '{}' in {}".format(topic_name, NOTIFICATION_CONFIG))
        topic = topics[topic_name]

    apikey = get_secret('mailgun_apikey')
    domain = get_secret('mailgun_domain')

    markdown_body = markdown_body.strip()
    payload = {
        'from': "dataland@{}".format(domain),
        'to': topic['subscribers'],
        'subject': topic['title'],
        'text': markdown_body,
        'html': markdown(markdown_body),
    }

    if os.environ.has_key('DATALAND_TEST') and os.environ['DATALAND_TEST'] == 'TRUE':
        return payload

    response = requests.post(
        "{}/{}/messages".format(MAILGUN_URL, domain),
        auth=HTTPBasicAuth(MAILGUN_USER, apikey),
        data=payload
    )
    if not response.ok:
        logger.error('Could not send notification on topic: {}'.format(topic_name))
