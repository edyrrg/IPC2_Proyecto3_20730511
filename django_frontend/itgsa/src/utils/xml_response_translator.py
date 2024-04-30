import xml.etree.ElementTree as ET


class XMLResponseTranslator:
    @staticmethod
    def translate_xml_response_config(response):
        process = ET.fromstring(response)
        # process customers response
        response_customers = process.find('Customers')
        created_customers = response_customers.find('Created').text
        updated_customers = response_customers.find('Updated').text
        # process banks response
        response_banks = process.find('Banks')
        created_banks = response_banks.find('Created').text
        updated_banks = response_banks.find('Updated').text

        response_processed = (f"Customers created: {created_customers}\n"
                              f"Customers updated: {updated_customers}\n"
                              f"\n"
                              f"Banks created: {created_banks}\n"
                              f"Banks updated: {updated_banks}\n")

        return response_processed

    @staticmethod
    def translate_xml_response_transactions(response):
        process = ET.fromstring(response)
        # process invoice response
        response_invoices = process.find('Invoices')
        created_invoices = response_invoices.find('NewInvoices').text
        duplicated_invoices = response_invoices.find('DuplicatedInvoices').text
        invoices_with_errors = response_invoices.find('InvoicesWithErrors').text
        # process payments reponse
        response_payments = process.find('Payments')
        created_payments = response_payments.find('NewPayments').text
        duplicated_payments = response_payments.find('DuplicatedPayments').text
        payment_with_errors = response_payments.find('PaymentWithErrors').text

        response_processed = ""
        return ""
