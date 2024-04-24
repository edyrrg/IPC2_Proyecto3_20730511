from abc import ABC, abstractmethod


# Template Create and Update Entity
class EntityCRUDBService(ABC):
    @abstractmethod
    def add_entity(self, entity):
        pass

    @abstractmethod
    def update_child(self, code, name):
        pass
