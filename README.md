# RabbitMQ fake email sender task (Homework №8.2)

## How to use?

### Using
1. Make your own `config.ini` file in `fake_email_sender_rabbitmq` directory
2. Run `python producer.py` to fill the db with fake contacts and send messages to the RabbitMQ queue 
3. Run `python consumer.py` to recieve messages, send fake emails and update contacts 'message_sent' status in the db