import json
from typing import List, Callable

import requests
from requests import Response

from business.repositories.interfaces.i_twitter_repository import ITwitterRepository
from enterprise.models.filter_rule import FilterRule
from enterprise.models.tweet import Tweet
from infrastructure.exception.http_exception import HttpException

from config import BEARER_TOKEN

TWITTER_URL = "https://api.twitter.com/2"
TWITTER_STREAM_URL = TWITTER_URL + "/tweets/search/stream"


class TwitterRepository(ITwitterRepository):
    @staticmethod
    def __requests_bearer_oauth(r: requests.Request) -> requests.Request:
        r.headers["Authorization"] = f"Bearer {BEARER_TOKEN}"
        r.headers["User-Agent"] = "TwitterStreamExtractor"
        return r

    @staticmethod
    def __convert_raw_data_to_filter_rule(data) -> List[FilterRule]:
        return [FilterRule(rule) for rule in data]

    @staticmethod
    def __convert_raw_data_to_tweet(raw_data) -> Tweet:
        return Tweet(raw_data["data"])

    @staticmethod
    def __handle_error(response: Response, expected_status_code: int):
        if response.status_code != expected_status_code:
            raise HttpException(response.status_code, response.text)

    def get_stream_rules(self) -> List[FilterRule]:
        url = TWITTER_STREAM_URL + "/rules"

        # Get Data
        response = requests.get(url, auth=TwitterRepository.__requests_bearer_oauth)

        # Handle error
        TwitterRepository.__handle_error(response, 200)

        # Parse Data
        response_content = response.json()

        # Convert data to FilterRule
        return TwitterRepository.__convert_raw_data_to_filter_rule(
            response_content.get("data", [])
        )

    def delete_stream_rules_by_ids(self, ids: List[int]) -> None:
        url = TWITTER_STREAM_URL + "/rules"

        # Create Payload
        payload = {"delete": {"ids": ids}}

        # Execute request
        response = requests.post(
            url,
            json=payload,
            auth=TwitterRepository.__requests_bearer_oauth,
        )

        # Handle error
        TwitterRepository.__handle_error(response, 200)

    def add_rules(self, rules: List[FilterRule]) -> List[FilterRule]:
        url = TWITTER_STREAM_URL + "/rules"

        # Create Payload
        payload = {"add": [rule.__dict__ for rule in rules]}

        # Execute request
        response = requests.post(
            url,
            json=payload,
            auth=TwitterRepository.__requests_bearer_oauth,
        )

        # Handle error
        TwitterRepository.__handle_error(response, 201)

        # Parse Data
        response_content = response.json()

        # Convert data to FilterRule
        return TwitterRepository.__convert_raw_data_to_filter_rule(
            response_content.get("data", [])
        )

    def stream_rules(self, callback_function: Callable[[Tweet], None]) -> None:
        url = TWITTER_STREAM_URL + "?tweet.fields=context_annotations,lang"
        print(url)
        response = requests.get(
            url,
            auth=TwitterRepository.__requests_bearer_oauth,
            stream=True,
        )

        # Handle error
        TwitterRepository.__handle_error(response, 200)

        # Stream
        for response_line in response.iter_lines():
            if response_line:
                # Parse Data
                json_response = json.loads(response_line)
                tweet = TwitterRepository.__convert_raw_data_to_tweet(json_response)

                # Callable
                callback_function(tweet)
