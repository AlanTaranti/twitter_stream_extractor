import abc
from typing import List, Callable

from src.enterprise.models.filter_rule import FilterRule
from src.enterprise.models.tweet import Tweet


class ITwitterStreamService(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_stream_rules(self) -> List[FilterRule]:
        raise NotImplementedError

    @abc.abstractmethod
    def delete_all_stream_rules(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def add_rules(self, rules: List[FilterRule]) -> List[FilterRule]:
        raise NotImplementedError

    @abc.abstractmethod
    def stream_rules(self, callback_function: Callable[[Tweet], None]) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def stream_with_rules(
        self,
        rules: List[FilterRule] | FilterRule,
        callback_function: Callable[[Tweet], None],
    ) -> None:
        raise NotImplementedError
