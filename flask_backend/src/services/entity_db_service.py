from abc import ABC, abstractmethod


class EntityDBService(ABC):
    @abstractmethod
    def add_entity(self, entity):
        pass
