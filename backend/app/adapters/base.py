from abc import ABC, abstractmethod


class BaseAdapter(ABC):
    @abstractmethod
    def load(self, *args, **kwargs) -> list[dict]:
        pass