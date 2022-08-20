from typing import List
import math

import fire

import pandas as pd

from src.application.controllers.implementation import TwitterStreamController
from src.business.services.implementation import TwitterStreamService
from src.infrastructure.repositories.implementation import TwitterRepository


def run(rules, output):
    """
    Extracts tweets containing designated rules and saves in parquet file.

    :param rules: List of rules to be used in the extraction. See how to define a rule on https://developer.twitter.com/en/docs/twitter-api/tweets/filtered-stream/integrate/build-a-rule.
    :param output: Filename of output parquet file.
    """
    repository = TwitterRepository()
    service = TwitterStreamService(repository)
    controller = TwitterStreamController(service)

    controller.stream_with_rule(rules, output)


def run_emoji(output):
    """
    Extracts tweets containing one or more emojis of Emoji Sentiment Ranking and saves in parquet file.

    :param output: Filename of output parquet file.
    """
    emojis = pd.read_csv("emoji_sentiment_data.csv")["emoji"].values
    emojis = ['"{}"'.format(emoji) for emoji in emojis]

    rules = []
    emoji_slice_size = 30
    passos = math.ceil(len(emojis) / emoji_slice_size)
    for i in range(passos):
        emoji_slice = emojis[i * emoji_slice_size : (i + 1) * emoji_slice_size]
        rule = "( " + " OR ".join(emoji_slice) + ")" + " lang:pt -is:retweet"
        rules.append(rule)

    run(rules, output)


if __name__ == "__main__":
    fire.Fire(
        {
            "run": run,
            "run-emoji": run_emoji,
        }
    )
