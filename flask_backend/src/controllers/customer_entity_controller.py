from src.controllers.entity_controller import EntityController
from src.entities.customer import Customer
from src.services.customers_db_service import CustomersDBService
import re


class CustomerEntityController(EntityController):
    PATRON_NIT = r'\b\d{8,}-[\dA-Z]\b'

    def __init__(self):
        self.customer_db_service: CustomersDBService = CustomersDBService()
        self.customer: Customer = None

    def create_entities(self, tag_customer):
        count_customers_created = 0
        count_customers_updated = 0
        for customer_xml in tag_customer:
            tmp_nit = str(customer_xml.find("NIT").text).strip().upper()
            name = str(customer_xml.find("nombre").text).strip()
            if not tmp_nit or not name:
                continue
            nit = re.search(self.PATRON_NIT, tmp_nit).group(0)
            print(nit)
            self.customer = Customer(nit, name)
            if self.customer_db_service.add_entity(new_customer=self.customer):
                count_customers_updated += 1
            else:
                count_customers_created += 1
        return count_customers_created, count_customers_updated
