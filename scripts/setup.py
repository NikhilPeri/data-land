import os

print '===(1/4) Installing System Dependencies==='
SYSTEM_DEPENDENCIES=[
    'git',
    'python',
    'python-pip',
    'systemd',
    'systemctl',
]
print os.system('sudo apt-get install {}'.format(' '.join(SYSTEM_DEPENDENCIES)))

print '===(2/4) Installing Python Dependencies==='
print os.system('sudo pip install -r requirements.txt')

print '===(3/4) Setup Google Service Account  ==='
# TODO

print '===(4/4)   Installing System Service   ==='
SERVICE='''[Unit]
Description=Dataland Scheduler
After=multi-user.target

[Service]
Type=idle
ExecStart=cd {} && /usr/bin/python -m dataland.scheduler &

[Install]
WantedBy=multi-user.target
'''.format(os.getcwd())

with open('/lib/systemd/system/dataland.service') as service:
    service.write(SERVICE)

os.system('sudo chmod 644 /lib/systemd/system/dataland.service')
os.system('sudo systemctl daemon-reload')
os.system('sudo systemctl enable dataland.service')

print '===      DONE - reboot when ready      ==='
