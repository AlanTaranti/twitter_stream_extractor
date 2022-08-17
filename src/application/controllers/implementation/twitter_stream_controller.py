from os import path, makedirs, system
from typing import Optional, List

import pandas as pd

from src.business.services.interfaces import ITwitterStreamService
from src.config import BASE_DIR
from src.enterprise.models.filter_rule import FilterRule
from src.enterprise.models.tweet import Tweet


class TwitterStreamController:
    def __init__(self, twitter_stream_service: ITwitterStreamService):
        self.tweet_count_to_save = 100

        self.twitter_stream_service = twitter_stream_service
        self.dataset: Optional[pd.DataFrame] = None
        self.tweet_count: int = 0
        self.output_dir: str = ""

    def load_dataset(self) -> pd.DataFrame:
        filepath = self.get_save_filepath()

        if path.exists(filepath):
            dataset = pd.read_parquet(filepath)
            self.tweet_count: int = dataset.shape[0]
            return dataset

        return pd.DataFrame(columns=["id", "text"])

    def save_tweet(self, tweet: Tweet) -> None:
        tweet_dataframe = pd.DataFrame(
            pd.Series(
                {
                    "id": tweet.id,
                    "text": tweet.text,
                }
            )
        ).T

        self.dataset = pd.concat([self.dataset, tweet_dataframe], axis=0)
        self.tweet_count += 1

    def get_save_filepath(self) -> str:
        filename = "tweets.parquet.gzip"

        directory = path.join(BASE_DIR, "..", self.output_dir)
        makedirs(directory, exist_ok=True)

        filepath = path.join(directory, filename)
        return filepath

    def save_dataframe_to_disk(self) -> None:
        filepath = self.get_save_filepath()

        self.dataset.to_parquet(filepath, compression="gzip")

    def process_tweet(self, tweet: Tweet) -> None:
        self.save_tweet(tweet)

        if self.tweet_count % self.tweet_count_to_save / 2 == 0:
            system("clear")
            print(f"{self.tweet_count} tweets processed")

        if self.tweet_count % self.tweet_count_to_save == 0:
            self.save_dataframe_to_disk()
            print(f"{self.tweet_count} tweets saved on disk")

    def stream_with_rule(self, rules: str | List[str], output_dir: str) -> None:
        self.output_dir = output_dir
        self.dataset = self.load_dataset()

        if not isinstance(rules, list):
            rules = [rules]

        filter_rules = [FilterRule({"value": rule}) for rule in rules]
        self.twitter_stream_service.stream_with_rules(filter_rules, self.process_tweet)
