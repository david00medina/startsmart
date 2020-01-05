from abc import ABC, abstractmethod


class AbstractWriter(ABC):
    @abstractmethod
    def write(self, data):
        pass

    @abstractmethod
    def release(self):
        pass
