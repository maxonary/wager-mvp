import os
from dotenv import load_dotenv

def load_env():
    load_dotenv()
    return {
        'API_KEY': os.getenv('API_KEY'),
        "MONGO_URI": os.getenv("MONGO_URI")
    }