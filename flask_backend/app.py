from datetime import datetime

from flask import Flask, send_from_directory, request, jsonify, Response
import xml.etree.ElementTree as ET

from src.controllers.bank_entity_controller import BankEntityController
from src.controllers.customer_entity_controller import CustomerEntityController
from src.controllers.invoice_entity_controller import InvoiceEntityController
from src.controllers.payment_entity_controller import PaymentEntityController
from src.services.banks_db_service import BanksDBService
from src.services.customers_db_service import CustomersDBService
from src.services.invoices_db_service import InvoicesDBService
from src.services.payments_db_service import PaymentsDBService
from src.utils.api_response_xml_builder import ApiResponseXMLBuilder
from src.utils.general_utils import GeneralUtils

app = Flask(__name__)

BASE_API_URL = 'api/v1'
# setting db connection and manage entities
bank_db = BanksDBService()
customer_db = CustomersDBService()
invoice_db = InvoicesDBService()
payments_db = PaymentsDBService()
bank_entity_controller = BankEntityController()
customer_entity_controller = CustomerEntityController()
invoice_entity_controller = InvoiceEntityController()
payment_entity_controller = PaymentEntityController()


@app.route(f'/{BASE_API_URL}/config', methods=['POST'])
def config():
    try:
        # Get XML request
        xml_data = request.data

        # Validate root tag, root tag must be "transacciones"
        root = ET.fromstring(xml_data)
        if root.tag != 'config':
            raise Exception(f'Invalid XML request - expected <config>, got <{root.tag}>')
        # Customers manage
        customers = root.find("clientes")

        count_customers_created, count_customers_updated = (customer_entity_controller
                                                            .create_entities(customers))

        # Banks manage
        banks = root.find("bancos")

        count_banks_created, count_banks_updated = bank_entity_controller.create_entities(banks)

        # build xml response
        xml_response = ApiResponseXMLBuilder.config(count_customers_created
                                                    , count_customers_updated
                                                    , count_banks_created
                                                    , count_banks_updated)
        # print("DATA RETORNADA:", xml_response)
        return xml_response, 200, {'Content-Type': 'application/xml'}
    except Exception as e:
        xml_response = ApiResponseXMLBuilder.basic(f"{str(e)}")
        return xml_response, 400, {'Content-Type': 'application/xml'}


@app.route(f'/{BASE_API_URL}/transaction', methods=['POST'])
def transaction():
    try:
        # Get XML request
        xml_data = request.data
        if customer_db.is_db_empty() and bank_db.is_db_empty():
            raise Exception('DB Customer and DB Bank are empty, please upload file config first')
        # Validate root tag, root tag must be "config"
        root = ET.fromstring(xml_data)
        if root.tag != 'transacciones':
            raise Exception(f'Invalid XML request - expected <transacciones>, got <{root.tag}>')
        # Invoice manage
        invoices = root.find("facturas")

        count_invoices_created, count_invoices_duplicated, count_invoices_with_errors = (invoice_entity_controller
                                                                                         .create_entities(invoices))

        # Payments manage
        payments = root.find("pagos")

        count_payments_created, count_payments_duplicated, count_payments_with_errors = (payment_entity_controller
                                                                                         .create_entities(payments))

        xml_response = ApiResponseXMLBuilder.transacciones(count_invoices_created,
                                                           count_invoices_duplicated,
                                                           count_invoices_with_errors,
                                                           count_payments_created,
                                                           count_payments_duplicated,
                                                           count_payments_with_errors)

        #print(customer_db.is_db_empty())
        #print(bank_db.is_db_empty())
        return xml_response, 200, {'Content-Type': 'application/xml'}
    except Exception as e:
        xml_response = ApiResponseXMLBuilder.basic(f"{str(e)}")
        return xml_response, 404, {'Content-Type': 'application/xml'}


@app.route(f'/{BASE_API_URL}/reset_database/<int:confirmation>', methods=['GET'])
def reset_database(confirmation):
    try:
        if confirmation == 1:
            customer_db.reset_db()
            bank_db.reset_db()
            invoice_db.reset_db()
            payments_db.reset_db()
            xml_response = ApiResponseXMLBuilder.basic(f"Reset Database "
                                                       f"DB Customer, "
                                                       f"DB Banks, "
                                                       f"DB Invoices, "
                                                       f"DB Payments")
            return xml_response, 200, {'Content-Type': 'application/xml'}
        xml_response = ApiResponseXMLBuilder.basic("400 Bad Request - Databases not restarted because the confirmation "
                                                   "is invalid")
        return xml_response, 400, {'Content-Type': 'application/xml'}
    except Exception as e:
        return f'Error: {str(e)}', 500


@app.route(f'/{BASE_API_URL}/customers/<customer_nit>', methods=['GET'])
def customers(customer_nit):
    try:
        if customer_db.is_db_empty() and bank_db.is_db_empty():
            raise Exception('404: DB Customer and DB Bank are empty, please upload file config first')
        if not customer_nit:
            raise Exception('400: Bad Request - No customer nit provided')

        customer_nit = str(customer_nit).strip()

        if not customer_db.is_entity_exist(customer_nit):
            raise Exception('404: No customer nit exists in the database DBCustomer')

        customer_tree = customer_db.get_customer_tree_by_id(customer_nit)

        invoices_customer_tree = invoice_db.get_invoices_by_nit(customer_nit)

        payments_customer_tree = payments_db.get_payments_by_nit(customer_nit)

        xml_response = ApiResponseXMLBuilder.response_customer_resume(customer_tree,
                                                                      invoices_customer_tree,
                                                                      payments_customer_tree)
        return xml_response, 200, {'Content-Type': 'application/xml'}
    except Exception as e:
        xml_response = ApiResponseXMLBuilder.basic(f"{str(e)}")
        return xml_response, 400, {'Content-Type': 'application/xml'}


@app.route(f'/{BASE_API_URL}/customers/all', methods=['GET'])
def all_customers():
    try:
        if customer_db.is_db_empty() and bank_db.is_db_empty():
            raise Exception('404: DB Customer and DB Bank are empty, please upload file config first')
        if invoice_db.is_db_empty() and payments_db.is_db_empty():
            raise Exception('404: DB Invoices and DB Payments are empty, please upload file transacciones first')
        list_all_customers = customer_db.get_all_customers()
        list_all_customers_resume = []
        for customer_el in list_all_customers:
            if (invoice_db.exist_invoices_with_this_nit(customer_el.nit) or
                    payments_db.exist_payments_with_this_nit(customer_el.nit)):
                customer_tree = customer_db.get_customer_tree_by_id(customer_el.nit)
                if invoice_db.exist_invoices_with_this_nit(customer_el.nit):
                    invoices_customer_tree = invoice_db.get_invoices_by_nit(customer_el.nit)
                    customer_tree.append(invoices_customer_tree)
                if payments_db.exist_payments_with_this_nit(customer_el.nit):
                    payments_customer_tree = payments_db.get_payments_by_nit(customer_el.nit)
                    customer_tree.append(payments_customer_tree)
                list_all_customers_resume.append(customer_tree)
        xml_response = ApiResponseXMLBuilder.response_all_customers_resume(list_all_customers_resume)
        return xml_response, 200, {'Content-Type': 'application/xml'}
    except Exception as e:
        xml_response = ApiResponseXMLBuilder.basic(f"{str(e)}")
        return xml_response, 400, {'Content-Type': 'application/xml'}


@app.route(f'/{BASE_API_URL}/payments/<date>', methods=['GET'])
def payments_resumes(date):
    try:
        if customer_db.is_db_empty() and bank_db.is_db_empty():
            raise Exception('404: DB Customer and DB Bank are empty, please upload file config first')
        if invoice_db.is_db_empty() and payments_db.is_db_empty():
            raise Exception('404: DB Invoices and DB Payments are empty, please upload file transacciones first')

        list_all_banks = bank_db.get_all_banks()

        curr_date, prev_date, last_date = GeneralUtils.calculate_three_previous_months(date)

        resume_tag = ET.Element('ResumePayments')

        for el in list_all_banks:
            if payments_db.exist_payment_with_this_bank_code(el.code):
                payments_tree = payments_db.get_payments_by_bank_code(el.code)
                total_quantity_1 = 0
                total_quantity_2 = 0
                total_quantity_3 = 0
                for payment_el in payments_tree:
                    date_tmp = payment_el.find('Date').text
                    date = datetime.strptime(date_tmp, '%d/%m/%Y')
                    date = date.strftime('%m/%Y')
                    if date == curr_date:
                        total_quantity_1 += float(payment_el.find('Amount').text)
                    if date == prev_date:
                        total_quantity_2 += float(payment_el.find('Amount').text)
                    if date == last_date:
                        total_quantity_3 += float(payment_el.find('Amount').text)
                if total_quantity_1 > 0 or total_quantity_2 > 0 or total_quantity_3 > 0:
                    bank = ET.SubElement(resume_tag, 'Bank')
                    bank_name = ET.SubElement(bank, 'Name')
                    bank_name.text = el.name
                    if total_quantity_1 > 0:
                        # Resume 1
                        resume_1 = ET.SubElement(bank, 'Resume')
                        date_1 = ET.SubElement(resume_1, 'Date')
                        date_1.text = curr_date
                        total_amount_1 = ET.SubElement(resume_1, 'TotalAmount')
                        total_quantity_1 = "{:.2f}".format(total_quantity_1)
                        total_amount_1.text = str(total_quantity_1)
                    if total_quantity_2 > 0:
                        # Resume 2
                        resume_2 = ET.SubElement(bank, 'Resume')
                        date_2 = ET.SubElement(resume_2, 'Date')
                        date_2.text = prev_date
                        total_amount_2 = ET.SubElement(resume_2, 'TotalAmount')
                        total_quantity_2 = "{:.2f}".format(total_quantity_2)
                        total_amount_2.text = str(total_quantity_2)
                    if total_quantity_3 > 0:
                        # Resume 3
                        resume_3 = ET.SubElement(bank, 'Resume')
                        date_3 = ET.SubElement(resume_3, 'Date')
                        date_3.text = last_date
                        total_amount_3 = ET.SubElement(resume_3, 'TotalAmount')
                        total_quantity_3 = "{:.2f}".format(total_quantity_3)
                        total_amount_3.text = str(total_quantity_3)

        ET.indent(resume_tag)

        xml_response = ET.tostring(resume_tag, encoding='utf-8', method='xml', xml_declaration=True,
                                   short_empty_elements=False)
        return xml_response, 200, {'Content-Type': 'application/xml'}
    except Exception as e:
        xml_response = ApiResponseXMLBuilder.basic(f"{str(e)}")
        return xml_response, 400, {'Content-Type': 'application/xml'}


@app.errorhandler(404)
def not_found(error):
    xml_response = ApiResponseXMLBuilder.basic(f"{str(error)}")
    return xml_response, 404, {'Content-Type': 'application/xml'}


if __name__ == '__main__':
    app.run(debug=True)
