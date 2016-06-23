import datetime
import json
import requests
import pika
import dateutil.parser
import dateutil.tz

next_time = None
time_increment = 5
weather_url = 'http://api.wunderground.com/api/809e2b2cd1463ea3/conditions/q/62022.json'

creds = pika.PlainCredentials('pooltemp', 'pooltemp')
connection = pika.BlockingConnection(pika.ConnectionParameters('ssessner.com', credentials=creds))

channel = connection.channel()

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='pool.fanout',
                   routing_key='temperature',
                   queue=queue_name)


def next_measurement_time():
    now = datetime.datetime.utcnow()
    next_meas_time = datetime.datetime(year=now.year,
                                       month=now.month,
                                       day=now.day,
                                       hour=now.hour,
                                       minute=now.minute-now.minute%time_increment,
                                       tzinfo=dateutil.tz.tzutc())

    next_meas_time += datetime.timedelta(minutes=time_increment)
    print('Next measurement will be at {0}'.format(next_meas_time
                                                   .astimezone(dateutil.tz.tzlocal())
                                                   .strftime("%Y-%m-%d %H:%M")))
    return next_meas_time


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
    meas['local_epoch'] = datetime.datetime.isoformat(meas_time) + 'Z'
    meas['h2o_temp'] = float(temp)
    meas['air_temp'] = float(weather['current_observation']['temp_f'])
    meas['humidity'] = float(str.split(str(weather['current_observation']['relative_humidity']), '%')[0])
    meas['wind_speed'] = float(weather['current_observation']['wind_mph'])
    meas['wind_gusts'] = float(weather['current_observation']['wind_gust_mph'])
    meas['wind_direction'] = int(weather['current_observation']['wind_degrees'])
    meas['precipitation'] = float(weather['current_observation']['precip_1hr_in'])
    meas['pressure'] = float(weather['current_observation']['pressure_in'])
    return meas


def post_meas(meas):
    r = requests.post('http://pool.ssessner.com/api/meas', json=meas)
    if r.status_code == 200:
        print('Measurement logged successfully')
    else:
        print('Measurement failed to log')


def callback(ch, method, properties, body):
    status = json.loads(body.decode("utf-8"))

    global next_time
    time = dateutil.parser.parse(status['time'])
    temp = float(status['temp'])

    if time >= next_time:
        print('Logging')
        meas_time = datetime.datetime(year=time.year,
                                      month=time.month,
                                      day=time.day,
                                      hour=time.hour,
                                      minute=time.minute - time.minute % time_increment,
                                      tzinfo=dateutil.tz.tzutc())

        weather_data = download_weather_data()
        meas_dict = build_meas(meas_time, temp, weather_data)

        post_meas(meas_dict)

        next_time = next_measurement_time()

    print('At {0} the pool was {1} degrees.'.format(time
                                                    .astimezone(dateutil.tz.tzlocal())
                                                    .strftime("%Y-%m-%d %H:%M"), temp))


next_time = next_measurement_time()

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()




