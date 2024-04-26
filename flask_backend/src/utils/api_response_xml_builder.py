from xml.etree import ElementTree as ET


class ApiResponseXMLBuilder:

    @staticmethod
    def basic(msg):
        response = ET.Element('Response')
        message = ET.SubElement(response, 'Message')
        message.text = msg
        ET.indent(response)
        return ET.tostring(response, encoding='utf-8', method='xml', xml_declaration=True)

    @staticmethod
    def config(count_customer_created,
               count_customer_updated,
               count_bank_created,
               count_bank_updated):
        response = ET.Element('Response')
        # format xml to how many customers were created and updated
        customers = ET.SubElement(response, 'Customers')
        created_customers = ET.SubElement(customers, 'Created')
        created_customers.text = str(count_customer_created)
        updated_customers = ET.SubElement(customers, 'Updated')
        updated_customers.text = str(count_customer_updated)
        # format xml to how many banks were created and updated
        banks = ET.SubElement(customers, 'Banks')
        created_banks = ET.SubElement(banks, 'Created')
        created_banks.text = str(count_bank_created)
        updated_banks = ET.SubElement(banks, 'Updated')
        updated_banks.text = str(count_bank_updated)
        ET.indent(response)
        return ET.tostring(response, encoding='utf-8', method='xml', xml_declaration=True)

    @staticmethod
    def transacciones(count_invoice_created,
                      count_invoice_duplicated,
                      count_invoice_with_errors,
                      count_payments_created,
                      count_payments_duplicated,
                      count_payments_with_errors,):
        response = ET.Element('Transactions')
        # format xml to how many invoices were created, duplicated and with errors
        invoices = ET.SubElement(response, 'Invoices')
        created_invoices = ET.SubElement(invoices, 'NewInvoices')
        created_invoices.text = str(count_invoice_created)
        updated_invoices = ET.SubElement(invoices, 'DuplicatedInvoices')
        updated_invoices.text = str(count_invoice_duplicated)
        invoices_with_errors = ET.SubElement(invoices, 'InvoicesWithErrors')
        invoices_with_errors.text = str(count_invoice_with_errors)
        # format xml to how many payments were created, duplicated and with errors
        payments = ET.SubElement(invoices, 'Payments')
        created_payments = ET.SubElement(payments, 'NewPayments')
        created_payments.text = str(count_payments_created)
        updated_payments = ET.SubElement(payments, 'DuplicatedPayments')
        updated_payments.text = str(count_payments_duplicated)
        payments_with_errors = ET.SubElement(payments, 'PaymentsWithErrors')
        payments_with_errors.text = str(count_payments_with_errors)

        ET.indent(response)
        return ET.tostring(response, encoding='utf-8', method='xml', xml_declaration=True)
