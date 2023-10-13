from models import Contacts
import connect
from random import randint
import json
import faker
import pika

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='message_mock', exchange_type='direct')
channel.queue_declare(queue='message_queue', durable=True)
channel.queue_bind(exchange='message_mock', queue='message_queue')


def create_fake_contacts():
    fake_data = faker.Faker()
    fake_contacts = []
    number_of_contacts = randint(10, 15)

    for i in range(number_of_contacts):
        fake_name = fake_data.name()
        fake_email = fake_data.email()
        fake_contacts.append([fake_name, fake_email])

    return fake_contacts


def seed_func(fake_contacts):
    seeded_contacts_ids = []

    for contact in fake_contacts:
        c = Contacts(fullname=contact[0], email=contact[1]).save()
        seeded_contacts_ids.append(str(c.id))
    
    return seeded_contacts_ids


def add_to_queue(ids):
    message_id = 0
    for contact_id in ids:
        message_id += 1
        message = {
            "message_id": message_id,
            "contact_id": contact_id,
            "payload": f"Fake message №{message_id}"
        }

        channel.basic_publish(
            exchange='message_mock',
            routing_key='message_queue',
            body=json.dumps(message).encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
        print(" [x] Sent %r" % message)
    
    connection.close()


if __name__ == '__main__':
    seeded_contacts_ids = seed_func(create_fake_contacts())
    add_to_queue(seeded_contacts_ids)