import os
import time

hostname = '192.168.20.1'

response = os.system('ping -c 1 ' + hostname + ' >/dev/null 2>&1')

if response == 0:
    print(hostname + ' is up!')
else:
    print(hostname + ' is down!')

    with open('/home/pi/restart_history', 'a') as f:
        f.write(time.strftime('%D %H:%M') + ' Lost Connection. Restarting.\n')

    os.system('/sbin/shutdown -r now >/dev/null')
