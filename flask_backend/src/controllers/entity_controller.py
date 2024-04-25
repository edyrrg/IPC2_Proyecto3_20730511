from abc import ABC, abstractmethod

from src.services.xml_db_service import XMLDBService


class EntityController(ABC):

    @abstractmethod
    def create_entities(self, tag_child):
        pass
