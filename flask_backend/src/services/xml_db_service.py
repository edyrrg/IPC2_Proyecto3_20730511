import os
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod

from src.utils import constants


class XMLDBService(ABC):
    def __init__(self, path_file):
        self.path_file = path_file
        self.check_bd_file()
        self.tree = ET.parse(self.path_file)
        self.root = self.tree.getroot()

    def check_bd_file(self):
        if not os.path.exists(self.path_file):
            # print("DB File not exist: ", True)
            self.init_db()

    @abstractmethod
    def init_db(self):
        pass

    @abstractmethod
    def append_child(self, child):
        pass

    @abstractmethod
    def get_child_by_id(self, code):
        pass

    @abstractmethod
    def is_entity_exist(self, code):
        pass

    @abstractmethod
    def reset_db(self):
        pass

    def set_root(self):
        self.tree = ET.parse(self.path_file)
        self.root = self.tree.getroot()
