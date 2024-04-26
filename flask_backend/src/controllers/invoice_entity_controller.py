from datetime import datetime

from src.controllers.entity_controller import EntityController
from src.entities.invoice import Invoice
from src.services.customers_db_service import CustomersDBService
from src.services.invoices_db_service import InvoicesDBService
import re


class InvoiceEntityController(EntityController):
    PATRON_DATE = r"\b\d{2}/\d{2}/\d{4}\b"

    def __init__(self):
        self.invoice_db_service: InvoicesDBService = InvoicesDBService()
        self.customer_db_service: CustomersDBService = CustomersDBService()
        self.invoice: Invoice = None

    def create_entities(self, tag_invoices):
        count_invoices_created = 0
        count_invoices_duplicated = 0
        count_invoices_with_errors = 0
        for invoice_xml in tag_invoices:
            # processing invoice
            invoice_number = str(invoice_xml.find("numeroFactura").text).strip()
            if self.invoice_db_service.is_entity_exist(invoice_number):
                count_invoices_duplicated += 1
                continue
            # processing and validate if nit customer exist in DB Customer
            nit_customer = str(invoice_xml.find("NITcliente").text).strip()
            if not self.customer_db_service.is_entity_exist(nit_customer):
                count_invoices_with_errors += 1
                continue
            # processing and extract date from text
            invoice_date_tmp = str(invoice_xml.find("fecha").text).strip()
            invoice_date_tmp = re.search(self.PATRON_DATE, invoice_date_tmp).group(0)
            # invoice_date = datetime.strptime(invoice_date_tmp.group(), "%d/%m/%Y").date()
            # invoice_date = invoice_date.strftime("%d/%m/%Y")

            # processing and convert to float value
            invoice_value = str(invoice_xml.find("valor").text).strip()
            invoice_value = float(invoice_value)
            invoice_value = "{:.2f}".format(invoice_value)

            self.invoice_db_service.append_child(Invoice(invoice_number, nit_customer, invoice_date_tmp, invoice_value))
            count_invoices_created += 1
        return count_invoices_created, count_invoices_duplicated, count_invoices_with_errors
