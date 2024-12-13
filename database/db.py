import pymongo
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

try:
    mongo = pymongo.MongoClient(os.getenv('MONGO_URI'))
    # use the database already included in the MONGO_URI
    db = mongo.get_default_database()

    # database collections
    product_collection = db['product']
    user_collection = db['users']

    print("Connected")
except:
    print('connection failed')
