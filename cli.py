from typing import List
import math

import fire

import pandas as pd

from src.application.controllers.implementation import TwitterStreamController
from src.business.services.implementation import TwitterStreamService
from src.infrastructure.repositories.implementation import TwitterRepository


def run(rules: str | List[str]):
    repository = TwitterRepository()
    service = TwitterStreamService(repository)
    controller = TwitterStreamController(service)

    controller.stream_with_rule(rules, "output")


def run_emoji():
    emojis = pd.read_csv("emoji_sentiment_data.csv")["emoji"].values
    emojis = ['"{}"'.format(emoji) for emoji in emojis]

    rules = []
    emoji_slice_size = 30
    passos = math.ceil(len(emojis) / emoji_slice_size)
    for i in range(passos):
        emoji_slice = emojis[i * emoji_slice_size : (i + 1) * emoji_slice_size]
        rule = "( " + " OR ".join(emoji_slice) + ")" + " lang:pt -is:retweet"
        rules.append(rule)

    run(rules)


if __name__ == "__main__":
    fire.Fire(
        {
            "run": run,
            "run-emoji": run_emoji,
        }
    )
