from src.services.XMLDBService import XMLDBService
from src.utils import constants
import xml.etree.ElementTree as ET


class CustomerDBService(XMLDBService):
    def __init__(self):
        super().__init__(constants.PATH_BD_CUSTOMERS)

    def init_db(self):
        customers = ET.Element("Customers")
        tree = ET.ElementTree(customers)
        # to indent file
        ET.indent(tree)
        tree.write(constants.PATH_BD_CUSTOMERS, encoding="utf-8", xml_declaration=True, short_empty_elements=False)

    def append_child(self, new_item):
        pass

    def update_child(self, child):
        pass

    def get_child_by_id(self, _id):
        pass


if __name__ == '__main__':
    DBService = CustomerDBService()
    Customer = ET.Element("Customer")
    Name = ET.SubElement(Customer, "Name")
    Name.text = "Edy Rojas"
    DBService.append_child(Customer)
