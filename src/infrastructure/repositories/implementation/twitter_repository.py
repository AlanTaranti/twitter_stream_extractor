from typing import List

import requests

from business.repositories.interfaces.i_twitter_repository import ITwitterRepository
from enterprise.models.filter_rule import FilterRule
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

    def get_stream_rules(self) -> List[FilterRule]:
        url = TWITTER_STREAM_URL + "/rules"

        # Get Data
        response = requests.get(url, auth=TwitterRepository.__requests_bearer_oauth)
        if response.status_code != 200:
            raise HttpException(response.status_code, response.text)

        # Parse Data
        response_content = response.json()

        # Convert data to FilterRule
        return TwitterRepository.__convert_raw_data_to_filter_rule(
            response_content.get("data", [])
        )

    def delete_stream_rules_by_ids(self, ids: List[int]):
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
        if response.status_code != 200:
            raise HttpException(response.status_code, response.text)

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
        if response.status_code != 201:
            raise HttpException(response.status_code, response.text)

        # Parse Data
        response_content = response.json()

        # Convert data to FilterRule
        return TwitterRepository.__convert_raw_data_to_filter_rule(
            response_content.get("data", [])
        )
