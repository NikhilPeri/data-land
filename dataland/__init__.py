import yaml

NOTIFICATION_CONFIG = 'config/notifications.yml'
SECRETS_CONFIG = 'config/secrets.yml'

def get_secret(name):
    with open(SECRETS_CONFIG, 'r') as secrets_file:
        secrets = yaml.load(secrets_file)
        return secrets[name]

global config
with open('config/dataland.yml') as config_file:
    config = yaml.load(config_file)
