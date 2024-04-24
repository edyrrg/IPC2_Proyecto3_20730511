from src.entities.invoice import Invoice
from src.services.xml_db_service import XMLDBService
from src.utils import constants
import xml.etree.ElementTree as ET


class InvoicesDBService(XMLDBService):

    def __init__(self):
        super().__init__(constants.PATH_DB_INVOICES)

    def init_db(self):
        invoices = ET.Element("Invoices")
        tree = ET.ElementTree(invoices)
        # indent file
        ET.indent(tree)
        tree.write(constants.PATH_DB_INVOICES, encoding="utf-8", xml_declaration=True, short_empty_elements=False)

    def append_child(self, new_invoice: Invoice):
        invoice = ET.SubElement(self.root, "Invoice")
        # Create tag invoice id and add text
        invoice_id = ET.SubElement(invoice, "InvoiceID")
        invoice_id.text = str(new_invoice.id)
        # Create tag customer nit and add text
        customer_nit = ET.SubElement(invoice, "CustomerNIT")
        customer_nit.text = new_invoice.customer_nit
        # Create tag date and add text
        date = ET.SubElement(invoice, "Date")
        date.text = new_invoice.date.strftime("%d/%m/%Y")
        # Create tag amount and add text
        amount = ET.SubElement(invoice, "Amount")
        amount.text = float(new_invoice.amount)
        # add indent
        ET.indent(self.tree)
        self.tree.write(constants.PATH_DB_INVOICES, encoding="utf-8", xml_declaration=True, short_empty_elements=False)

    def get_child_by_id(self, _id):
        for invoice_el in self.root.findall('Invoice'):
            invoice_id = invoice_el.find('InvoiceID').text
            if invoice_id == str(_id):
                _id = invoice_el.find('InvoiceID').text
                customer_nit = invoice_el.find('CustomerNIT').text
                date = invoice_el.find('Date').text
                amount = invoice_el.find('Amount').text
                return Invoice(_id, customer_nit, date, amount)
        return None

    def is_entity_exist(self, _id):
        for invoice_el in self.root.findall('Invoice'):
            invoice_id = invoice_el.find('InvoiceID').text
            if invoice_id == str(_id):
                return True
        return False

    def reset_db(self):
        pass


if __name__ == '__main__':
    service = InvoicesDBService()
    service.init_db()
