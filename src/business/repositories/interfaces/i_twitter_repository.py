import abc
from typing import List

from enterprise.models.filter_rule import FilterRule


class ITwitterRepository(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_stream_rules(self) -> List[FilterRule]:
        raise NotImplementedError

    @abc.abstractmethod
    def delete_stream_rules_by_ids(self, ids: List[int]) -> None:
        raise NotImplementedError
