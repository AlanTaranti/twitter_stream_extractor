#
# Twitter Stream Extractor
#

## Import
import os
import sys
import tweepy
import logging
import pandas as pd
from time import sleep
from os.path import join, dirname
from dotenv import load_dotenv
from requests.exceptions import ConnectionError
from urllib3.exceptions import ReadTimeoutError
from urllib3.exceptions import ProtocolError

from listener.stream_listener import StreamListener

## Environment Variables
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

## Twitter Access
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token_key = os.getenv('ACCESS_TOKEN_KEY')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

language = os.getenv('ACCEPTED_LANGUAGE')
data_type = os.getenv('DATA_TYPE')
country_code_monitored = os.getenv('COUNTRY_CODE_MONITORED')  # Todo: Implementar


## Configure Logging
def configure_logging():
    pid = "/tmp/store_tweet.pid"
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    fh = logging.FileHandler("log", "w")
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    keep_fds = [fh.stream.fileno()]
    return logger


def get_api(logger):
    global consumer_key, consumer_secret, access_token_key, access_token_secret
    logger.debug("Authenticating")

    if not consumer_key or not consumer_secret or not access_token_key or not access_token_secret:
        print('Saindo! Estão Faltando Informações de Acesso ao Twitter')
        sys.exit(1)

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)
    api = tweepy.API(auth)

    return api


def get_emojis():
    emoji_data = pd.read_csv('emoji_sentiment_data.csv')
    return list(emoji_data['emoji'].values)


def get_emojis_simple():
    emoji_data = pd.read_csv('simple_emoji_sentiment_data.csv')
    return list(emoji_data['emoji'].values)


def start_stream(api, stream_listener, terms):
    while True:
        stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
        try:
            stream.filter(track=terms, languages=[language])
        except ConnectionError:
            print('Sem Rede! Aguardando 10 segundos para tentar novamente...')
            sleep(10)
        except ReadTimeoutError:
            continue
        except ProtocolError:
            continue


def start():
    logger = configure_logging()
    api = get_api(logger)

    # Start Listener
    logger.debug("Starting Listener")
    logger.debug("Starting Filter")

    # Get Terms
    terms = []
    if data_type == 'emoji':
        terms = get_emojis()
    elif data_type == 'emoji_simple':
        terms = get_emojis_simple()

    # Start Streamer
    stream_listener = StreamListener(logger, language)
    start_stream(api, stream_listener, terms)


if __name__ == '__main__':
    print('Executando Tweet Streaming...')
    start()
