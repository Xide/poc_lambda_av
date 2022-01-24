import io
import json
import time
import pika
import clamd
from minio import Minio
from minio.commonconfig import CopySource

cd = clamd.ClamdUnixSocket()
client = Minio("minio:9000", "minio", "minio123", secure=False)


def callback(ch, method, properties, body):
    delivery_tag = method.delivery_tag
    print("[DBG] %r" % body)
    payload = json.loads(body)
    for record in payload['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        try:
            resp = client.get_object(bucket, key)
            tag, malware_type = cd.instream(resp)['stream']
            print('[INFO]', bucket, key, ':', tag, malware_type)
            if tag == 'OK':
                result = client.copy_object(
                    "accepted",
                    key,
                    CopySource(bucket, key),
                )
            else:
                result = client.copy_object(
                    "rejected",
                    key,
                    CopySource(bucket, key),
                )
            client.remove_object(bucket, key)
        finally:
            resp.close()
            resp.release_conn()

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='rabbitmq',
    credentials=pika.PlainCredentials('myuser', 'mypassword')
))
channel = connection.channel()
channel.exchange_declare(
    exchange='exchange',
    exchange_type='fanout'
)
result = channel.queue_declare('test', exclusive=False)
queue_name = result.method.queue
channel.queue_bind(exchange='exchange',
                   queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')
channel.basic_consume(queue_name, callback, auto_ack=True)
channel.start_consuming()
