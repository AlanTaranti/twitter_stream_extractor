from typing import List

from business.repositories.interfaces import ITwitterRepository
from enterprise.models.filter_rule import FilterRule


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

    def add_rules(self, rules: List[FilterRule]) -> List[FilterRule]:
        return self.twitter_repository.add_rules(rules)
