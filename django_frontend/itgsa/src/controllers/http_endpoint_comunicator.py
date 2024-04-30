import xml.etree.ElementTree as ET
import requests


class HttpEndpointComunicator:
    HEADERS = {'Content-Type': 'application/xml'}

    @staticmethod
    def send_config(data):
        ET.indent(data)
        data_formated = ET.tostring(data)
        url_config_endpoint = "http://127.0.0.1:5000/api/v1/config"
        response = requests.post(url_config_endpoint, headers=HttpEndpointComunicator.HEADERS, data=data_formated)
        return response

    @staticmethod
    def send_transactions(data):
        ET.indent(data)
        data_formated = ET.tostring(data)
        url_transactions_endpoint = "http://127.0.0.1:5000/api/v1/transaction"
        response = requests.post(url_transactions_endpoint, headers=HttpEndpointComunicator.HEADERS, data=data_formated)
        return response
