import os
from dotenv import load_dotenv

def load_env():
    load_dotenv()
    return {
        'API_KEY': os.getenv('API_KEY_Campus'),
        "MONGO_URI": os.getenv("MONGO_URI")
    }