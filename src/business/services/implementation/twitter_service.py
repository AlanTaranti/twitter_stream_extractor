from typing import List

from business.repositories.interfaces.i_twitter_repository import ITwitterRepository
from enterprise.models.filter_rule import FilterRule
from infrastructure.repositories.implementation.twitter_repository import TwitterRepository


class TwitterService:

    def __init__(self, twitter_repository: ITwitterRepository):
        self.twitter_repository = twitter_repository

    def get_stream_rules(self) -> List[FilterRule]:
        return self.twitter_repository.get_stream_rules()

    def delete_all_stream_rules(self) -> None:
        rules = self.twitter_repository.get_stream_rules()

        if len(rules) == 0:
            return

        ids = [rule.id for rule in rules]

        self.twitter_repository.delete_stream_rules_by_ids(ids)


if __name__ == "__main__":
    from pprint import pprint

    twitter_service = TwitterService(twitter_repository=TwitterRepository())
    pprint(twitter_service.get_stream_rules())
    twitter_service.delete_all_stream_rules()
    pprint(twitter_service.get_stream_rules())
