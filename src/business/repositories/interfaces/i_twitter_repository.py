import abc
from typing import List, Callable

from enterprise.models.filter_rule import FilterRule
from enterprise.models.tweet import Tweet


class ITwitterRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_stream_rules(self) -> List[FilterRule]:
        raise NotImplementedError

    @abc.abstractmethod
    def delete_stream_rules_by_ids(self, ids: List[int]) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def add_rules(self, rules: List[FilterRule]) -> List[FilterRule]:
        raise NotImplementedError

    @abc.abstractmethod
    def stream(self, callback_function: Callable[[Tweet], None]) -> None:
        raise NotImplementedError
