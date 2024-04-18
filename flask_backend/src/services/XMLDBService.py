import os
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod

from src.utils import constants


class XMLDBService(ABC):
    def __init__(self, path_file):
        self.path_file = path_file
        self.check_bd_file()
        self.root = ET.parse(self.path_file).getroot()

    def check_bd_file(self):
        if not os.path.exists(self.path_file):
            self.init_db()

    @abstractmethod
    def init_db(self):
        pass
        #customers = ET.Element("Customers")

        #tree = ET.ElementTree(customers)
        # para intentar el archivo
        #ET.indent(tree)

        #tree.write(constants.PATH_BD_CUSTOMERS, encoding="utf-8", xml_declaration=True, short_empty_elements=False)

    @abstractmethod
    def append_child(self, child):
        pass

    @abstractmethod
    def update_child(self, child):
        pass

    @abstractmethod
    def get_child_by_id(self, _id):
        pass
