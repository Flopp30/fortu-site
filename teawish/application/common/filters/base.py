import abc
from typing import Any


class BaseEllipsisFilter(abc.ABC):
    @property
    def filter_dict(self) -> dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if v is not Ellipsis}
