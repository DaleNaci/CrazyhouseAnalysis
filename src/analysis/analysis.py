from abc import ABC, abstractmethod


class Analysis(ABC):
    @abstractmethod
    def run(self):
        pass