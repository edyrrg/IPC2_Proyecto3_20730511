# from abc import ABC
import os
import xml.etree.ElementTree as ET
import xml.dom.minidom

from src.utils import constants


class XMLDBService:
    def __init__(self):
        pass

    def check_file(self):
        if not os.path.exists(constants.PATH_BD_CUSTOMERS):
            self.create_db_file()

    def create_db_file(self):
        customers = ET.Element("Customers")

        tree = ET.ElementTree(customers)
        # para intentar el archivo
        #ET.indent(tree)

        tree.write(constants.PATH_BD_CUSTOMERS, encoding="utf-8", xml_declaration=True, short_empty_elements=False)


if __name__ == "__main__":
    service = XMLDBService()
    service.create_db_file()
