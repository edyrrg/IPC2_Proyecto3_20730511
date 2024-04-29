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
        self.set_root()
        invoice = ET.SubElement(self.root, "Invoice")
        # Create tag invoice id and add text
        invoice_id = ET.SubElement(invoice, "InvoiceID")
        invoice_id.text = str(new_invoice.id)
        # Create tag customer nit and add text
        customer_nit = ET.SubElement(invoice, "CustomerNIT")
        customer_nit.text = new_invoice.customer_nit
        # Create tag date and add text
        date = ET.SubElement(invoice, "Date")
        date.text = new_invoice.date
        # Create tag amount and add text
        amount = ET.SubElement(invoice, "Amount")
        amount.text = new_invoice.amount
        # add indent
        ET.indent(self.tree)
        self.tree.write(constants.PATH_DB_INVOICES, encoding="utf-8", xml_declaration=True, short_empty_elements=False)

    def get_child_by_id(self, _id):
        self.set_root()
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
        self.set_root()
        for invoice_el in self.root.findall('Invoice'):
            invoice_id = invoice_el.find('InvoiceID').text
            if invoice_id == str(_id):
                return True
        return False

    def reset_db(self):
        self.root.clear()
        invoice = ET.Element("Invoices")
        tree = ET.ElementTree(invoice)
        # indent file
        ET.indent(tree)
        tree.write(constants.PATH_DB_INVOICES, encoding="utf-8", xml_declaration=True, short_empty_elements=False)

    def get_invoices_by_nit(self, nit):
        self.set_root()
        invoices = self.root.findall('Invoice')
        invoices_customer = ET.Element('Invoices')
        for invoice_el in invoices:
            if str(invoice_el.find('CustomerNIT').text).strip() == nit:
                invoice = ET.SubElement(invoices_customer, "Invoice")
                # create element xml to InvoiceID
                invoice_id = ET.SubElement(invoice, "InvoiceID")
                invoice_id.text = invoice_el.find('InvoiceID').text
                # create element xml to Customer NIT
                customer_nit = ET.SubElement(invoice, "CustomerNIT")
                customer_nit.text = invoice_el.find('CustomerNIT').text
                # create element xml to Date
                date = ET.SubElement(invoice, "Date")
                date.text = invoice_el.find('Date').text
                # create element xml to Amount
                amount = ET.SubElement(invoice, "Amount")
                amount.text = invoice_el.find('Amount').text
        return invoices_customer

    def exist_invoice_with_this_nit(self, nit):
        self.set_root()
        invoices = self.root.findall('Invoice')
        for invoice_el in invoices:
            invoice_nit = invoice_el.find('CustomerNIT').text
            if str(nit).strip() == str(invoice_nit).strip():
                return True
        return False

    def is_db_empty(self):
        self.set_root()
        if not self.root.findall('Invoice'):
            return True
        return False


if __name__ == '__main__':
    service = InvoicesDBService()
    service.init_db()
