import os
from pymongo import MongoClient
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

username = quote_plus(os.getenv("MONGO_USERNAME", ""))
password = quote_plus(os.getenv("MONGO_PASS", ""))
cluster = os.getenv("MONGO_CLUSTER", "cluster0.r7qrj.mongodb.net")
db_name = os.getenv("MONGO_DB_NAME", "Kunal")
app_name = os.getenv("APP_NAME", "Cluster0")

MONGO_URI = f"mongodb+srv://{username}:{password}@{cluster}/{db_name}?retryWrites=true&w=majority&appName={app_name}"

client = MongoClient(MONGO_URI)
db = client[db_name]
