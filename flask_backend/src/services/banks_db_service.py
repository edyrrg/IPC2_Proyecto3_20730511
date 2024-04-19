from src.entities.bank import Bank
from src.services.xml_db_service import XMLDBService
from src.services.entity_db_service import EntityDBService
from src.utils import constants
import xml.etree.ElementTree as ET


class BankDBService(XMLDBService, EntityDBService):

    def __init__(self):
        super().__init__(constants.PATH_DB_BANKS)

    def init_db(self):
        banks = ET.Element("Banks")
        tree = ET.ElementTree(banks)
        # indent file
        ET.indent(tree)
        tree.write(constants.PATH_DB_BANKS, encoding="utf-8", xml_declaration=True, short_empty_elements=False)

    def append_child(self, new_bank: Bank):
        bank = ET.SubElement(self.root, "Bank")
        # Create tag code and add text
        code = ET.SubElement(bank, "Code")
        code.text = new_bank.code
        # Create tag name and add text
        name = ET.SubElement(bank, "Name")
        name.text = new_bank.name
        # add indent
        ET.indent(self.tree)
        self.tree.write(constants.PATH_DB_BANKS, encoding="utf-8", xml_declaration=True, short_empty_elements=False)

    def update_child(self, code, name):
        bank_to_update = self.get_child_by_id(code)
        if bank_to_update:
            if name:
                bank_to_update.name = name

            # Update data in bank_db_customer.xml
            for bank_el in self.root.findall('Bank'):
                cliente_id = bank_el.find('Code').text
                if cliente_id == str(code):
                    bank_el.find('Name').text = bank_to_update.name
                    break
            self.tree.write(constants.PATH_DB_BANKS, encoding="utf-8",
                            xml_declaration=True, short_empty_elements=False)
            return True
        else:
            return False

    def get_child_by_id(self, code):
        for bank_el in self.root.findall('Bank'):
            bank_code = bank_el.find('Code').text
            if bank_code == str(code):
                code = bank_el.find('Code').text
                name = bank_el.find('Name').text
                return Bank(code, name)
        return None

    def is_entity_exist(self, code):
        for customer_el in self.root.findall('Bank'):
            cliente_id = customer_el.find('Code').text
            if cliente_id == str(code):
                return True
        return False

    def add_entity(self, new_bank: Bank):
        if self.is_entity_exist(new_bank.code):
            self.update_child(new_bank.code, new_bank.name)
            return True
        else:
            self.append_child(new_bank)
            return False


if __name__ == '__main__':
    BDService = BankDBService()
    bank_sample = Bank("B001", "BanColombia")
    BDService.add_entity(bank_sample)
    bank_find = BDService.get_child_by_id("B001")
    print(bank_find)
    bank_exist = BDService.is_entity_exist("B001")
    print(bank_exist)
    bank_sample = Bank("B005", "BI")
    BDService.add_entity(bank_sample)
    bank_find = BDService.get_child_by_id("B005")
    print(bank_find)
    bank_exist = BDService.is_entity_exist("B005")
    print(bank_exist)
    #BDService.init_db()
