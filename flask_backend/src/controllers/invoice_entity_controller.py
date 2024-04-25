from src.controllers.entity_controller import EntityController
from src.entities.invoice import Invoice
from src.services.customers_db_service import CustomersDBService
from src.services.invoices_db_service import InvoicesDBService


class InvoiceEntityController(EntityController):
    def __init__(self):
        self.invoice_db_service: InvoicesDBService = InvoicesDBService()
        self.customer_db_service: CustomersDBService = CustomersDBService()
        self.invoice: Invoice = None

    def create_entities(self, tag_invoices):
        count_invoices_created = 0
        count_invoices_duplicated = 0
        count_invoices_with_errors = 0
        for invoice_xml in tag_invoices:
            invoice_number = invoice_xml.find("numeroFactura").text
            nit_customer = invoice_xml.find("NITcliente").text
            invoice_date = invoice_xml.find("fecha").text
            invoice_value = invoice_xml.find("valor").text
            print(invoice_number, nit_customer, invoice_date, invoice_value)
