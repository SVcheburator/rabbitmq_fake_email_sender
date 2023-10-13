from mongoengine import connect
import configparser


config = configparser.ConfigParser()
config.read('config.ini')

mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'pass')


# connect to cluster on AtlasDB with connection string
connect(host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@cluster0.versbmk.mongodb.net/""", ssl=True)