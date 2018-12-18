import yaml

CONFIG_FILE = 'config/dataland.yml'
NOTIFICATION_CONFIG = 'config/notifications.yml'
global config
with open(CONFIG_FILE, 'r') as config_file:
    config = yaml.load(config_file)
