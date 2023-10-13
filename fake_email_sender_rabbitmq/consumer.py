from models import Contacts
import connect
import pika
import time
import json

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='message_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

def send_email(contact_id):
    time.sleep(0.5)
    
    contact = Contacts.objects(id=contact_id)
    contact.update(message_sent=True)


def callback(ch, method, properties, body):
    message = json.loads(body.decode())
    print(f" [x] Received {message}")
    print(" [x] Sending email...")
    send_email(message['contact_id'])
    print(f" [x] Email has been sent successfully!\n [x] Email content: '{message['payload']}'\n")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='message_queue', on_message_callback=callback)


if __name__ == '__main__':
    channel.start_consuming()