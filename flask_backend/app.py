from flask import Flask, send_from_directory, request, jsonify, Response
import xml.etree.ElementTree as ET
from src.services.banks_db_service import BankDBService
from src.services.customers_db_service import CustomerDBService
from src.services.invoices_db_service import InvoicesDBService
from src.services.payments_db_service import PaymentsDBService

app = Flask(__name__)

BASE_API_URL = 'api/v1'
# setting db connection and manage
bank_db = BankDBService()
customer_db = CustomerDBService()
invoice_db = InvoicesDBService()
payments_db = PaymentsDBService()


@app.route(f'/{BASE_API_URL}/config', methods=['POST'])
def config():
    try:
        # Obtener los datos XML de la solicitud
        xml_data = request.data
        print("DATA RECEIVED: ", xml_data)

        # Procesar los datos XML
        root = ET.fromstring(xml_data)
        print("XML RECEIVED: ", root)

        # Crear el resultado final como XML
        response = ET.Element('Response')
        result_customers = ET.SubElement(response, 'customers')
        result_banks = ET.SubElement(response, 'banks')
        result_banks.text = "Hello"
        result_customers.text = "Hello"

        # Convertir el resultado final a XML
        ET.indent(response)
        xml_response = ET.tostring(response, encoding='utf-8', method='xml', xml_declaration=True)

        print("DATA RETORNADA:", xml_response)

        return xml_response, 200, {'Content-Type': 'application/xml'}
    except Exception as e:
        print(f'Error: {str(e)}', 400)
        return f'Error: {str(e)}', 400


@app.route(f'/{BASE_API_URL}/transaction', methods=['GET'])
def transaction():
    try:
        # Obtener los datos XML de la solicitud
        xml_data = request.data
        print("DATA RECEIVED: ", xml_data)

        # Procesar los datos XML
        root = ET.fromstring(xml_data)
        print("XML RECEIVED: ", root)

        # Crear el resultado final como XML
        response = ET.Element('Response')
        result_customers = ET.SubElement(response, 'customers')
        result_banks = ET.SubElement(response, 'banks')
        result_banks.text = "Hello"
        result_customers.text = "Hello"

        # Convertir el resultado final a XML
        ET.indent(response)
        xml_response = ET.tostring(response, encoding='utf-8', method='xml', xml_declaration=True)

        print("DATA RETORNADA:", xml_response)

        return xml_response, 200, {'Content-Type': 'application/xml'}
    except Exception as e:
        print(f'Error: {str(e)}', 400)
        return f'Error: {str(e)}', 400


@app.route(f'/{BASE_API_URL}/reset_database/<int:confirmation>', methods=['GET'])
def reset_database(confirmation):
    try:
        if confirmation == 1:
            customer_db.init_db()
            bank_db.init_db()
            invoice_db.init_db()
            payments_db.init_db()
            response = ET.Element('Response')
            message = ET.SubElement(response, 'Message')
            message.text = (f"Reset Database "
                            f" DB Customer, "
                            f"DB Banks, "
                            f"DB Invoices, "
                            f"DB Payments")
            ET.indent(response)
            xml_response = ET.tostring(response, encoding='utf-8', method='xml', xml_declaration=True)
            return xml_response, 200, {'Content-Type': 'application/xml'}
        response = ET.Element('Response')
        message = ET.SubElement(response, 'Message')
        message.text = f"400 Bad Request: Databases not restarted because the confirmation is invalid"
        ET.indent(response)
        xml_response = ET.tostring(response, encoding='utf-8', method='xml', xml_declaration=True)
        return xml_response, 400, {'Content-Type': 'application/xml'}
    except Exception as e:
        return f'Error: {str(e)}', 500


@app.errorhandler(404)
def not_found(error):
    response = ET.Element('Response')
    message = ET.SubElement(response, 'Message')
    message.text = f"{str(error)}"
    ET.indent(response)
    xml_response = ET.tostring(response, encoding='utf-8', method='xml', xml_declaration=True)
    return xml_response, 404, {'Content-Type': 'application/xml'}


if __name__ == '__main__':
    app.run(debug=True)
