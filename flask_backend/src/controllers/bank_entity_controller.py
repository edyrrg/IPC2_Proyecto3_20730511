from src.controllers.entity_controller import EntityController
from src.entities import bank
from src.entities.bank import Bank
from src.services.banks_db_service import BanksDBService


class BankEntityController(EntityController):
    def __init__(self):
        self.bank_db_service: BanksDBService = BanksDBService()
        self.bank: Bank = None

    def create_entities(self, tag_banks):
        count_banks_created = 0
        count_banks_updated = 0
        for bank_xml in tag_banks:
            code = str(bank_xml.find("codigo").text).strip()
            name = str(bank_xml.find("nombre").text).strip()
            if not code and not name:
                continue
            self.bank = Bank(code, name)
            if self.bank_db_service.add_entity(new_bank=self.bank):
                count_banks_updated += 1
            else:
                count_banks_created += 1
        return count_banks_created, count_banks_updated
