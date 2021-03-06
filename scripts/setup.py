import os

print '===(1/4) Installing System Dependencies==='
SYSTEM_DEPENDENCIES=[
    'git',
    'python',
    'python-pip',
    'python-dev',
    'systemd',
]
print os.system('sudo apt-get install {}'.format(' '.join(SYSTEM_DEPENDENCIES)))
swap_size = raw_input('Enter swap partition size in GB (enter 0 to skip), recommended if system memory less than 1GB')
try:
    swap_size = int(swap_size)
    if swap_size < 1:
        raise
    os.system('sudo fallocate -l {}G /swapfile')
    os.system('sudo chmod 600 /swapfile; sudo mkswap /swapfile; sudo swapon /swapfile; sudo swapon -s')
    os.system('sudo echo "swapfile none swap sw 0 0" >> /etc/fstab')
except:
    pass

try:
    os.makedirs('logs')
except:
    pass

print '===(2/4) Installing Python Dependencies==='
print os.system('sudo pip install -r requirements.txt')

print '===(3/4) Setup dataland/config.yml  ==='
def setup_config():
    import yaml
    config={
        'storage': {
            'gcloud_bucket': 'data-land',
            'gcloud_credentials': raw_input('Path to GCloud credential file').strip(),
        },
        'notification': {
            'mailgun_apikey': raw_input('Mailgun API key').strip(),
            'mailgun_domain': raw_input('Mailgun Domain').strip()
        }
    }
    with open('config/dataland.yml', 'w+') as config_file:
        yaml.dump(config, config_file)

setup_config()

print '===(4/4)   Installing System Service   ==='
SCHEDULER_SCRIPT='scripts/scheduler'
with open(SCHEDULER_SCRIPT, 'w+') as scheduler_script:
    scheduler_script.write('cd {} && /usr/bin/python -m dataland.scheduler'.format(os.getcwd()))
os.system('sudo chmod +x {}'.format(SCHEDULER_SCRIPT))

SERVICE='''[Unit]
Description=Dataland Scheduler
After=multi-user.target

[Service]
Type=idle
ExecStart=/bin/bash {}

[Install]
WantedBy=multi-user.target
'''.format(os.path.join(os.getcwd(), SCHEDULER_SCRIPT))

with open('/lib/systemd/system/dataland.service', 'w+') as service:
    service.write(SERVICE)


os.system('sudo chmod 644 /lib/systemd/system/dataland.service')
os.system('sudo systemctl daemon-reload')
os.system('sudo systemctl enable dataland.service')

print '===      DONE - reboot when ready      ==='
