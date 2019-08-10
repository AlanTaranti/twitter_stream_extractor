## Import
import tweepy
import pandas as pd
from time import time


class StreamListener(tweepy.StreamListener):

    def __init__(self, logger, language=None, api=None):
        self.logger = logger  # Inicializa o Logger

        self.total = 0
        self.language = language

        # Save Control
        self.processed_tweets_counter = 0
        self.processed_tweets_to_save = 10
        self.save_file = 'raw_data'
        self.save_location = 'data/' + self.save_file + '.gzip'

        # Backup Control
        self.save_count_to_backup = 5000
        self.elapsed_time_to_save = 600
        self.save_count = 0
        self.start_time = time()

        self.raw_tweet = None
        self.raw_tweet = self.load_raw_tweet()

        super().__init__(api)

    def load_raw_tweet(self):
        self.logger.debug("Loading Tweets")
        try:
            with open(self.save_location, 'r'):
                raw_tweets = pd.read_parquet(self.save_location)
                self.total = len(raw_tweets)
                self.logger.debug("Stored Tweets: " + str(self.total))
        except IOError:
            raw_tweets = pd.DataFrame()
        return raw_tweets

    def save_raw_tweet(self):
        self.raw_tweet.to_parquet(self.save_location, compression='gzip')
        self.save_count += 1

        if self.save_count == self.save_count_to_backup or time() - self.start_time > self.elapsed_time_to_save:
            self.raw_tweet.to_parquet(self.save_location + '_bkp', compression='gzip')
            self.save_count = 0
            self.start_time = time()

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

        self.processed_tweets_counter += 1
        self.total += 1
        self.logger.debug('Total Tweets: ' + str(self.total))

        # Armazena no disco
        if self.processed_tweets_counter > self.processed_tweets_to_save:
            self.logger.debug("Saving on Disk")
            self.save_raw_tweet()
            self.processed_tweets_counter = 0

        self.logger.debug("Waiting for Tweet")
