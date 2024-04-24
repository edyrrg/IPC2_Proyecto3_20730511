from xml.etree import ElementTree as ET


class ApiResponseXmlBuilder:

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
