from abc import ABC, abstractmethod


class IRepository(ABC):

    @abstractmethod
    def get_action(self, key):
        pass

    @abstractmethod
    def target(self, key):
        pass

    @abstractmethod
    def get_metric(self, key):
        pass

    @abstractmethod
    def get_certification(self, key):
        pass

    @abstractmethod
    def get_technology(self, key):
        pass

    @abstractmethod
    def get_alias(self, key):
        pass

    @abstractmethod
    def get_domain(self, key):
        pass

    @abstractmethod
    def get_semantics(self):
        pass