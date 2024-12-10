import pymongo
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

try:
    mongo = pymongo.MongoClient(os.getenv('MONGO_URI'))
    db = mongo.get_default_database()
    product_collection = db['product']
    print("Connected")
except:
    print('connection failed')
