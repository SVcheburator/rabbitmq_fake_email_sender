from mongoengine import Document
from mongoengine.fields import StringField, BooleanField

class Contacts(Document):
    fullname = StringField()
    email = StringField()
    message_sent = BooleanField(default=False)
