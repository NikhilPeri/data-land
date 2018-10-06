import os

print '===(1/1)     Remove System Service     ==='
os.system('sudo systemctl disable dataland.service')
os.system('sudo rm /lib/systemd/system/dataland.service')
os.system('sudo systemctl daemon-reload')
