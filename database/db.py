import pymongo
from dotenv import load_dotenv
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load the .env file
load_dotenv()

try:
    mongo = pymongo.MongoClient(os.getenv('MONGO_URI'))
    # use the database already included in the MONGO_URI
    db = mongo.get_default_database()

    # database collections
    product_collection = db['product']
    user_collection = db['users']

    logging.info("Connected to MongoDB successfully.")
except:
    logging.error("Connection to MongoDB failed.", exc_info=True)
