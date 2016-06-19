import glob
from datetime import datetime, tzinfo, timedelta
import pika
import time
import json

status = dict()
status['time'] = datetime.utcnow().isoformat() + 'Z'

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'


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

status['temp'] = read_temp('f')

creds = pika.PlainCredentials('pooltemp', 'pooltemp')
connection = pika.BlockingConnection(pika.ConnectionParameters('ssessner.com', credentials=creds))
channel = connection.channel()

channel.queue_declare(queue='pool')

message = json.dumps(status)

channel.basic_publish(exchange='pool.fanout',
                      routing_key='temperature',
                      body=message
                      )

connection.close()
