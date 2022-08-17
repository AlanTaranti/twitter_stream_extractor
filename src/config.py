from os import environ
from os.path import join, dirname, realpath

from dotenv import load_dotenv

# Load Environment Variables
dotenv_path = join(dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)

# Configs
BEARER_TOKEN = environ.get("BEARER_TOKEN")

BASE_DIR = dirname(realpath(__file__))
