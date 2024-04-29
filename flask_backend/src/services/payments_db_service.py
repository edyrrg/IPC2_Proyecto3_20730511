from src.entities.payment import Payment
from src.services.xml_db_service import XMLDBService
from src.utils import constants
import xml.etree.ElementTree as ET


class PaymentsDBService(XMLDBService):

    def __init__(self):
        super().__init__(constants.PATH_DB_PAYMENTS)

    def init_db(self):
        payments = ET.Element("Payments")
        tree = ET.ElementTree(payments)
        # indent file
        ET.indent(tree)
        tree.write(constants.PATH_DB_PAYMENTS, encoding="utf-8", xml_declaration=True, short_empty_elements=False)

    def append_child(self, new_payment: Payment):
        self.set_root()
        payment = ET.SubElement(self.root, "Payment")
        # Create tag bank code and add text
        bank_code = ET.SubElement(payment, "BankCode")
        bank_code.text = new_payment.bank_code
        # Create tag customer nit and add text
        customer_nit = ET.SubElement(payment, "CustomerNIT")
        customer_nit.text = new_payment.customer_nit
        # Create tag date and add text
        date = ET.SubElement(payment, "Date")
        date.text = new_payment.date
        # Create tag amount and add text
        amount = ET.SubElement(payment, "Amount")
        amount.text = new_payment.amount
        # add indent
        ET.indent(self.tree)
        self.tree.write(constants.PATH_DB_PAYMENTS, encoding="utf-8", xml_declaration=True, short_empty_elements=False)

    def get_child_by_id(self, payment: Payment):
        self.set_root()
        for payment_el in self.root.findall('Payment'):
            bank_code = payment_el.find('BankCode').text
            customer_nit = payment_el.find('CustomerNIT').text
            date = payment_el.find('Date').text
            if (bank_code == str(payment.bank_code)
                    and customer_nit == str(payment.customer_nit)
                    and date == payment.date.strftime("%d/%m/%Y")):
                bank_code = payment_el.find('InvoiceID').text
                customer_nit = payment_el.find('CustomerNIT').text
                date = payment_el.find('Date').text
                amount = payment_el.find('Amount').text
                return Payment(bank_code, customer_nit, date, amount)
        return None

    def is_entity_exist(self, payment: Payment):
        self.set_root()
        for payment_el in self.root.findall('Payment'):
            bank_code = payment_el.find('BankCode').text
            customer_nit = payment_el.find('CustomerNIT').text
            date = payment_el.find('Date').text
            if (bank_code == str(payment.bank_code)
                    and customer_nit == str(payment.customer_nit)
                    and date == payment.date):
                return True
        return False

    def reset_db(self):
        self.root.clear()
        payment = ET.Element("Payments")
        tree = ET.ElementTree(payment)
        # indent file
        ET.indent(tree)
        tree.write(constants.PATH_DB_PAYMENTS, encoding="utf-8", xml_declaration=True, short_empty_elements=False)

    def get_payments_by_nit(self, nit):
        self.set_root()
        payments = self.root.findall('Payment')
        payments_customer = ET.Element('Payments')
        for payment_el in payments:
            if str(payment_el.find('CustomerNIT').text).strip() == nit:
                payment = ET.SubElement(payments_customer, "Payment")
                # create element xml to InvoiceID
                invoice_id = ET.SubElement(payment, "BankCode")
                invoice_id.text = payment_el.find('BankCode').text
                # create element xml to Customer NIT
                customer_nit = ET.SubElement(payment, "CustomerNIT")
                customer_nit.text = payment_el.find('CustomerNIT').text
                # create element xml to Date
                date = ET.SubElement(payment, "Date")
                date.text = payment_el.find('Date').text
                # create element xml to Amount
                amount = ET.SubElement(payment, "Amount")
                amount.text = payment_el.find('Amount').text
        return payments_customer

    def exist_invoice_with_this_nit(self, nit):
        self.set_root()
        payments = self.root.findall('Payment')
        for payment_el in payments:
            invoice_nit = payment_el.find('CustomerNIT').text
            if str(nit).strip() == str(invoice_nit).strip():
                return True
        return False

    def is_db_empty(self):
        self.set_root()
        if not self.root.findall('Payment'):
            return True
        return False


if __name__ == '__main__':
    service = PaymentsDBService()
    service.init_db()
