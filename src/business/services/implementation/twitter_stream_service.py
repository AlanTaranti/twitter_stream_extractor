from typing import List, Callable

from src.business.repositories.interfaces import ITwitterRepository
from src.business.services.interfaces import ITwitterStreamService
from src.enterprise.models.filter_rule import FilterRule
from src.enterprise.models.tweet import Tweet


class TwitterStreamService(ITwitterStreamService):
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

    def add_rules(self, rules: List[FilterRule] | FilterRule) -> List[FilterRule]:
        if not isinstance(rules, list):
            rules = [rules]

        return self.twitter_repository.add_rules(rules)

    def stream_rules(self, callback_function: Callable[[Tweet], None]) -> None:
        self.twitter_repository.stream_rules(callback_function)

    def stream_with_rules(
        self,
        rules: List[FilterRule] | FilterRule,
        callback_function: Callable[[Tweet], None],
    ) -> None:
        self.delete_all_stream_rules()
        self.add_rules(rules)
        self.stream_rules(callback_function)
