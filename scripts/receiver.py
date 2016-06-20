
import pika
import json
import datetime
import dateutil.parser
import dateutil.tz

creds = pika.PlainCredentials('pooltemp', 'pooltemp')
connection = pika.BlockingConnection(pika.ConnectionParameters('ssessner.com', credentials=creds))

channel = connection.channel()

# channel.exchange_declare(exchange='amq.fanout',
#                         type='fanout')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='pool.fanout',
                   routing_key='temperature',
                   queue=queue_name)


def callback(ch, method, properties, body):
    status = json.loads(body)

    time = dateutil.parser.parse(status['time']).replace(tzinfo=dateutil.tz.tzutc()).astimezone(dateutil.tz.tzlocal())
    temp = float(status['temp'])
    print('At {0} the pool was {1} degrees.'.format(time, temp))

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
