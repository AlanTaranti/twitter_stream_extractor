from os import environ
from os.path import join, dirname

from dotenv import load_dotenv

# Environment Variables
dotenv_path = join(dirname(__file__), '..', ".env")
load_dotenv(dotenv_path)

BEARER_TOKEN = environ.get("BEARER_TOKEN")
