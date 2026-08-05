from abc import ABC
from abc import abstractmethod


class ScoreEngineBase(ABC):

    def __init__(self):

        pass

    @abstractmethod
    def score(self, evidence):

        raise NotImplementedError