import requests
from requests.auth import HTTPBasicAuth

from markdown2 import markdown

NOTIFICATION_CONFIG = 'config/notifications.yml'
MAILGUN_URL = 'https://api.mailgun.net/v3/'
MAILGUN_USER = 'api'

class NotificationInterface(object):
    def notify(notification):
        raise NotImplemented

class MailgunInterface(NotificationInterface):
    def __init__(self):
        with open(NOTIFICATION_CONFIG, 'r') as notification_config:
            config = yaml.load(notification_config)
            self.apikey = config['mailgun_apikey']
            self.domain = config['mailgun_domain']
            self.topics = config['topics']

    def notify(self, topic, markdown_body):
        if not self.topics.haskey(topic):
            raise ValueError("Could finde topic '{}' in {}".format(topic, NOTIFICATION_CONFIG))

        payload = {
            'from': "notifications@{}".format(self.domain),
            'to': self.topic[topic]['subscribers'],
            'subject': self.topic[topic]['title'],
            'text': markdown_body,
            'html': markdown(markdown_body),
        }

        if os.environ.haskey('DATALAND_TEST') and os.environ['DATALAND_TEST'] == 'TRUE':
            return payload
        else:
            requests.post(
                "{}/{}/messages".format(MAILGUN_URL, self.domain),
                auth=HTTPBasicAuth(MAILGUN_USER, self.apikey),
                data=payload
            )
