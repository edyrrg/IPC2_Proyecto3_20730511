import re

from src.entities.customer import Customer
from src.services.customers_db_service import CustomerDBService


class CustomerEntityController:

    def __init__(self):
        self.customer_db_service: CustomerDBService = CustomerDBService()
        self.customer: Customer = None

    def create_customers_entities(self, tag_banks):
        count_customers_created = 0
        count_customers_updated = 0
        for customer_xml in tag_banks:
            code = customer_xml.find("NIT").text
            name = customer_xml.find("nombre").text
            self.customer = Customer(code, name)
            if self.customer_db_service.add_entity(new_customer=self.customer):
                count_customers_updated += 1
            else:
                count_customers_created += 1
        return count_customers_created, count_customers_updated
