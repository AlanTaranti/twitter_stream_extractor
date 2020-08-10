## Import
import tweepy
import os.path
import pandas as pd
from time import time


class StreamListener(tweepy.StreamListener):

    def __init__(self, logger, language=None, api=None):
        self.logger = logger  # Inicializa o Logger

        self.total = 0
        self.session_total = 0
        self.language = language

        # Save Control
        self.processed_tweets_to_save = 3000
        self.save_directory = 'data/'
        self.save_file = 'raw_data'
        self.save_location = self.save_directory + self.save_file + '.gzip'

        # Backup Control
        self.processed_tweets_to_backup = 6000
        self.elapsed_time_to_save = 600
        self.last_save_time = time()

        self.raw_tweet = None
        self.raw_tweet = self.load_raw_tweet()

        # Info control
        self.start_time = time()

        super().__init__(api)

    def load_raw_tweet(self):
        self.logger.debug("Loading Tweets")
        load_location = self.save_location

        if not os.path.isfile(load_location):
            load_location = load_location + '_bkp'

        try:
            with open(load_location, 'r'):
                raw_tweets = pd.read_parquet(load_location)
                self.total = len(raw_tweets)
                self.logger.debug("Stored Tweets: " + str(self.total))
        except IOError:
            raw_tweets = pd.DataFrame()
        return raw_tweets

    def save_raw_tweet(self):

        if not os.path.isdir(self.save_directory):
            os.mkdir(self.save_directory)

        self.raw_tweet.to_parquet(self.save_location, compression='gzip')

        if self.session_total % self.processed_tweets_to_save == 0 or time() - self.last_save_time > self.elapsed_time_to_save:
            self.raw_tweet.to_parquet(self.save_location + '_bkp', compression='gzip')
            self.last_save_time = time()

    # Override
    # Analisa o tweet
    def on_status(self, status):

        # Filtrar o tweet
        if not self.filter_tweet(status):
            return

        # Processar o tweet
        response = self.process_tweet(status)

        # Armazenar o tweet
        self.store_tweet(response)

    # Override
    # Valida erros
    def on_error(self, status_code):

        # Codigo 420, jah atingiu o limite de solicitação
        # Retorn False, que encerra a solicitação
        if status_code == 420:
            self.logger.logger.debug("ERROR: Status Code - 420")
            return False

    # Filtra o tweet
    def filter_tweet(self, status):
        # Converte o status em um dicionario
        # Para analisar as chaves
        d = dict(status._json)

        # Remover os retweets
        if 'retweeted_status' in d and status.retweeted_status:
            return False

        # Ignore idioma não selecionado
        if self.language is not None and 'lang' not in d or status.lang != self.language:
            return False

        self.logger.debug("Tweet Accepted")

        return True

    # Processa o tweet
    def process_tweet(self, status):

        self.logger.debug("Processing a Tweet")

        # Converte o status em um dicionario
        # Para analisar as chaves
        d = dict(status._json)

        # Transforma os dados relevantes em um dicionario
        response = dict()
        response['status_id_str'] = status.id_str
        response['status_text'] = status.text
        response['status_creation'] = status.created_at
        # response['status_retweets'] = status.retweet_count
        # response['status_favorited'] = status.favorite_count if 'favorite_count' in d else None
        if 'place' not in d:
            response['country'] = None
        elif d['place'] is None or 'country_code' not in d['place']:
            response['country'] = None
        else:
            response['country'] = status.place.country_code
        # response['user_description'] = status.user.description if 'description' in d else None
        response['user_name'] = status.user.screen_name
        response['user_creation'] = status.user.created_at
        response['user_followers'] = status.user.followers_count

        return response

    # Armazena o tweet
    def store_tweet(self, response):

        self.logger.debug("Storing a Tweet")

        # Armazena no DataFrame
        self.raw_tweet = self.raw_tweet.append(response, ignore_index=True)

        self.session_total += 1
        self.total += 1
        self.logger.debug('Total Tweets: ' + str(self.total))

        self.show_info()

        # Armazena no disco
        if self.session_total % self.processed_tweets_to_save == 0:
            self.logger.debug("Saving on Disk")
            self.save_raw_tweet()

        self.logger.debug("Waiting for Tweet")

    def show_info(self):
        os.system('clear')
        print('Streaming...')
        print('Total Tweets:', self.total)
        print('Session Tweets:', self.session_total)
        elapsed_time = time() - self.start_time
        elapsed_hour = elapsed_time / 60 / 60
        tweets_per_hour = int(self.session_total / elapsed_hour)
        print('Speed: {} Tweets/hour'.format(tweets_per_hour))
