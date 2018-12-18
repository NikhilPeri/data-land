import yaml

CONFIG_FILE = 'config/dataland.yml'

global config
with open(CONFIG_FILE, 'r') as config_file:
    config = yaml.load(config_file)
