import datetime
import glob
import time
import urllib3
import json

meas_time = datetime.datetime.now()

#base_dir = '/sys/bus/w1/devices/'
#device_folder = glob.glob(base_dir + '28*')[0]
#device_file = device_folder + '/w1_slave'

#output_file = '/home/pi/temp_current'
#output_history_file = '/home/pi/temp_history'
#weather_file = '/home/pi/weather/'
#web_page_file = '/home/pi/web/index.html'

weather_url = 'http://api.wunderground.com/api/809e2b2cd1463ea3/conditions/q/62022.json'

def read_temp_raw():
    with open(device_file, 'r') as f:
    	lines = f.readlines()
    return lines

def read_temp(unit):
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        if unit == 'c':
            return temp_c
        elif unit == 'f':
            return temp_f
        else:
            raise Exception("Unit must be c or f")

def write_temp(t):
    with open(output_file,'w') as f:
    	f.write(meas_time.strftime('%D %H:%M') + ', ' + str(t) + '\n')

def write_temp_history(t):
    with open(output_history_file,'a') as f:
        f.write(meas_time.strftime('%D %H:%M') + ', ' + str(t) + '\n')

def update_web_page(temp, time):
    with open(web_page_file,'w') as w:
        w.writelines(['<html>',
            '<head>',
            '<title>Current Pool Temp</title>',
            '</head>',
            '<body bgcolor="white" text="black">',
            '<center><h1>The Pool is currently ' + str(int(round(temp,0))) + ' degrees</h1></center>',
            '<center><p>Last Updated at ' + time.strftime('%D %H:%M') + ' </p></center>',
            '</body>',
            '</html>'])

def download_weather_data():
    http = urllib3.PoolManager()
    response = http.request('get',weather_url)
    """:type : urllib3.HTTPResponse"""

    if(response.status == 200):
        # file_name = weather_file + meas_time.strftime('%Y%m%d%H')

        data = response.data.decode('utf8')
        jdata = json.loads(data)
        pass
        # with open(file_name,'a') as f:
        #    f.write(str(data))

#temp = read_temp('f')
#temp = round(temp,1)
#write_temp(temp)
#write_temp_history(temp)
download_weather_data()
#update_web_page(temp,meas_time)
