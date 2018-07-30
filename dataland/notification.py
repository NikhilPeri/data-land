import os
import yaml
import requests
from requests.auth import HTTPBasicAuth

from markdown2 import markdown

NOTIFICATION_CONFIG = 'config/notifications.yml'
MAILGUN_URL = 'https://api.mailgun.net/v3'
MAILGUN_USER = 'api'

class NotificationInterface(object):
    def notify(self, topic, markdown_body):
        raise NotImplemented

class MailgunNotification(NotificationInterface):
    def __init__(self):
        with open(NOTIFICATION_CONFIG, 'r') as notification_config:
            config = yaml.load(notification_config)
            self.apikey = config['mailgun_apikey']
            self.domain = config['mailgun_domain']
            self.topics = config['topics']

    def notify(self, topic_name, markdown_body):
        if not self.topics.has_key(topic_name):
            raise ValueError("Could find topic '{}' in {}".format(topic_name, NOTIFICATION_CONFIG))

        topic = self.topics[topic_name]
        payload = {
            'from': "dataland@{}".format(self.domain),
            'to': topic['subscribers'],
            'subject': topic['title'],
            'text': markdown_body,
            'html': markdown(markdown_body),
        }

        if os.environ.has_key('DATALAND_TEST') and os.environ['DATALAND_TEST'] == 'TRUE':
            return payload

        response = requests.post(
            "{}/{}/messages".format(MAILGUN_URL, self.domain),
            auth=HTTPBasicAuth(MAILGUN_USER, self.apikey),
            data=payload
        )
        if not response.ok:
            logger.error('Could not send notification on topic: {}'.format(topic_name))
