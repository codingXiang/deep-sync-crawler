from dotenv import load_dotenv
import os

load_dotenv()

def get(key):
    return os.environ.get(key)
