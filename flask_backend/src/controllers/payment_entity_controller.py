from src.controllers.entity_controller import EntityController
from src.entities.payment import Payment
from src.services.banks_db_service import BanksDBService
from src.services.customers_db_service import CustomersDBService
from src.services.payments_db_service import PaymentsDBService
import re


class PaymentEntityController(EntityController):
    PATRON_DATE = r"\b\d{2}/\d{2}/\d{4}\b"

    def __init__(self):
        self.payment_db_service: PaymentsDBService = PaymentsDBService()
        self.customer_db_service: CustomersDBService = CustomersDBService()
        self.banks_db_service: BanksDBService = BanksDBService()
        self.payment: Payment = None

    def create_entities(self, tag_payment):
        count_payments_created = 0
        count_payments_duplicated = 0
        count_payments_with_errors = 0
        for payment_xml in tag_payment:
            # processing and validate if bank code exist in DB Bank
            bank_code = str(payment_xml.find('codigoBanco').text).strip()
            if not self.banks_db_service.is_entity_exist(bank_code):
                count_payments_with_errors += 1
                continue
            # processing payment date
            payment_date = str(payment_xml.find('fecha').text).strip()
            payment_date = re.search(self.PATRON_DATE, payment_date).group(0)
            # processing and validate if nit customer exist in DB Customer
            customer_nit = str(payment_xml.find('NITcliente').text).strip()
            if not self.customer_db_service.is_entity_exist(customer_nit):
                count_payments_with_errors += 1
                continue
            # processing and convert to float value
            payment_amount = str(payment_xml.find('valor').text).strip()
            payment_amount = float(payment_amount)
            payment_amount = "{:.2f}".format(payment_amount)
            # processing and validate entity payment
            new_payment = Payment(bank_code, customer_nit, payment_date, payment_amount)
            if self.payment_db_service.is_entity_exist(new_payment):
                count_payments_duplicated += 1
                continue
            self.payment_db_service.append_child(new_payment)
            count_payments_created += 1
        return count_payments_created, count_payments_duplicated, count_payments_with_errors
