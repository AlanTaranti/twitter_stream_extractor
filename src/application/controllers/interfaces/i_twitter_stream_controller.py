import abc


class ITwitterStreamController(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def stream_with_rule(self, rule: str, output_dir: str) -> None:
        raise NotImplementedError
