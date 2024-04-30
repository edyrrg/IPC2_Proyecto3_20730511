from src.entities.customer import Customer
from src.services.xml_db_service import XMLDBService
from src.services.entity_cru_db_service import EntityCRUDBService
from src.utils import constants
import xml.etree.ElementTree as ET


class CustomersDBService(XMLDBService, EntityCRUDBService):

    def __init__(self):
        super().__init__(constants.PATH_BD_CUSTOMERS)

    def init_db(self):
        customers = ET.Element("Customers")
        tree = ET.ElementTree(customers)
        # indent file
        ET.indent(tree)
        tree.write(constants.PATH_BD_CUSTOMERS, encoding="utf-8", xml_declaration=True, short_empty_elements=False)

    def append_child(self, new_customer: Customer):
        self.set_root()
        customer = ET.SubElement(self.root, "Customer")
        # Create tag nit and add text
        nit = ET.SubElement(customer, "NIT")
        nit.text = new_customer.nit
        # Create tag name and add text
        name = ET.SubElement(customer, "Name")
        name.text = new_customer.name
        # add indent
        ET.indent(self.tree)
        self.tree.write(constants.PATH_BD_CUSTOMERS, encoding="utf-8", xml_declaration=True, short_empty_elements=False)

    def update_child(self, nit, name):
        self.set_root()
        customer_to_update = self.get_child_by_id(nit)
        if customer_to_update:
            if name:
                customer_to_update.name = name

            # Update data in db_customer.xml
            for customer_el in self.root.findall('Customer'):
                cliente_id = customer_el.find('NIT').text
                if cliente_id == str(nit):
                    customer_el.find('Name').text = customer_to_update.name
                    break
            self.tree.write(constants.PATH_BD_CUSTOMERS, encoding="utf-8",
                            xml_declaration=True, short_empty_elements=False)
        else:
            raise Exception("Customer not found then cannot update")

    def get_child_by_id(self, nit):
        self.set_root()
        for customer_el in self.root.findall('Customer'):
            cliente_id = customer_el.find('NIT').text
            if cliente_id == str(nit):
                nit = customer_el.find('NIT').text
                name = customer_el.find('Name').text
                return Customer(nit, name)
        return None

    def get_customer_tree_by_id(self, nit):
        self.set_root()
        for customer_el in self.root.findall('Customer'):
            cliente_id = customer_el.find('NIT').text
            if cliente_id == str(nit):
                customer_tree = ET.Element("Customer")
                nit = ET.SubElement(customer_tree, "NIT")
                nit.text = customer_el.find('NIT').text
                name = ET.SubElement(customer_tree, "Name")
                name.text = customer_el.find('Name').text
                return customer_tree
        return None

    def is_entity_exist(self, nit):
        self.set_root()
        for customer_el in self.root.findall('Customer'):
            cliente_id = customer_el.find('NIT').text
            if cliente_id == str(nit):
                return True
        return False

    def add_entity(self, new_customer: Customer):
        if self.is_entity_exist(new_customer.nit):
            self.update_child(new_customer.nit, new_customer.name)
            return True
        else:
            self.append_child(new_customer)
            return False

    def reset_db(self):
        self.root.clear()
        customers = ET.Element("Customers")
        tree = ET.ElementTree(customers)
        # indent file
        ET.indent(tree)
        tree.write(constants.PATH_BD_CUSTOMERS, encoding="utf-8", xml_declaration=True, short_empty_elements=False)

    def is_db_empty(self):
        self.set_root()
        if not self.root.findall('Customer'):
            return True
        return False

    def get_all_customers(self):
        self.set_root()
        list_customers = []
        all_customers = self.root.findall('Customer')
        for customer in all_customers:
            nit = customer.find('NIT').text
            name = customer.find('Name').text
            list_customers.append(Customer(nit, name))
            list_customers.append(Customer(nit, name))
        list_customers.sort(key=lambda x: x.nit)
        return list_customers


if __name__ == '__main__':
    DBService = CustomersDBService()

    customer_sample = Customer("10420876-6", "Rodrigo Leon Morales")
    DBService.add_entity(customer_sample)
    customer_find = DBService.get_child_by_id("10420876-6")
    print(customer_find)

    customer_sample = Customer("10420876-5", "Denilson Florentino")
    DBService.add_entity(customer_sample)
    customer_find = DBService.get_child_by_id("10420876-5")
    print(customer_find)

    customer_exist = DBService.is_entity_exist("10420876-5")
    print(customer_exist)
    #DBService.init_db()
