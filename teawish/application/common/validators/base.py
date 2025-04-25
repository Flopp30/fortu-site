import abc
from typing import TypeVar, Any, Generic


V = TypeVar('V', bound=Any)


class BaseValidator(Generic[V], abc.ABC):
    def __init__(self, v: V):
        self.value: V = v
        self._validate()

    @abc.abstractmethod
    def _validate(self): ...
