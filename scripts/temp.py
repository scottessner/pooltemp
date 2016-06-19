import glob
import datetime
import json
import requests
import pika

meas_time = datetime.datetime.now()

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

# output_file = '/home/pi/temp_current'
# output_history_file = '/home/pi/temp_history'
# weather_file = '/home/pi/weather/'
# web_page_file = '/home/pi/web/index.html'

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
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        if unit == 'c':
            return temp_c
        elif unit == 'f':
            return temp_f
        else:
            raise Exception("Unit must be c or f")


def write_temp(t):
    with open(output_file, 'w') as f:
        f.write(meas_time.strftime('%D %H:%M') + ', ' + str(t) + '\n')


def write_temp_history(t):
    with open(output_history_file, 'a') as f:
        f.write(meas_time.strftime('%D %H:%M') + ', ' + str(t) + '\n')


def update_web_page(temp, time):
    with open(web_page_file, 'w') as w:
        w.writelines(['<html>',
                      '<head>',
                      '<title>Current Pool Temp</title>',
                      '</head>',
                      '<body bgcolor="white" text="black">',
                      '<center><h1>The Pool is currently ' + str(int(round(temp, 0))) + ' degrees</h1></center>',
                      '<center><p>Last Updated at ' + time.strftime('%D %H:%M') + ' </p></center>',
                      '</body>',
                      '</html>'])


def download_weather_data():
    r = requests.get(weather_url)

    jason_data = ''

    if r.status_code == 200:
        # file_name = weather_file + meas_time.strftime('%Y%m%d%H')
        data = r.text
        jason_data = json.loads(data)

    return jason_data


def build_meas(meas_time, temp, weather):
    meas = dict()
    meas['local_epoch'] = datetime.datetime.isoformat(meas_time)
    meas['h2o_temp'] = float(temp)
    meas['air_temp'] = float(weather['current_observation']['temp_f'])
    meas['humidity'] = float(str.split(str(weather['current_observation']['relative_humidity']),'%')[0])
    meas['wind_speed'] = float(weather['current_observation']['wind_mph'])
    meas['wind_gusts'] = float(weather['current_observation']['wind_gust_mph'])
    meas['wind_direction'] = int(weather['current_observation']['wind_degrees'])
    meas['precipitation'] = float(weather['current_observation']['precip_1hr_in'])
    meas['pressure'] = float(weather['current_observation']['pressure_in'])
    return meas


def post_meas(meas):
    r = requests.post('http://127.0.0.1/api/meas', json=meas)

temp = read_temp('f')

creds = pika.PlainCredentials('charger', 'charger')
connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1', credentials=creds))
channel = connection.channel()

channel.queue_declare(queue='batt')


weather_data = download_weather_data()
meas_dict = build_meas(meas_time, temp, weather_data)

post_meas(meas_dict)

