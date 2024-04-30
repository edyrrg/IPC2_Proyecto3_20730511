from django.shortcuts import render
import xml.etree.ElementTree as ET

from itgsa.src.controllers.http_endpoint_comunicator import HttpEndpointComunicator
from itgsa.src.utils.xml_response_translator import XMLResponseTranslator


# Create your views here.

def index(request):
    context = {'home_active': 'is-selected'}
    return render(request, 'index.html', context)


def reset_data_base(request):
    context = {'reset_db_active': 'is-selected',
               'response_active': 'response-not-active'}
    return render(request, 'reset_data_base.html', context)


def send_database_restart(request):
    context = {'reset_db_active': 'is-selected',
               'response_active': 'response-not-active'}
    return render(request, 'reset_data_base.html', context)


def student_data(request):
    context = {'student_data_active': 'is-selected'}
    return render(request, 'student_data.html', context)


def documentation(request):
    context = {'documentation_active': 'is-selected'}
    return render(request, 'documentation.html', context)


def load_file_configuration(request):
    context = {'load_file_configuration_active': 'is-selected',
               'response_active': 'response-not-active'}
    return render(request, 'load_file_configuration.html', context)


def load_file_transactions(request):
    context = {'load_file_transactions_active': 'is-selected',
               'response_active': 'response-not-active'}
    return render(request, 'load_file_transactions.html', context)


def process_file_config(request):
    context = {}
    if request.method == 'POST' and request.FILES['xml_file']:
        try:
            file = request.FILES['xml_file']
            data = file.read().decode('utf-8')
            xml_tree = ET.fromstring(data)
            if xml_tree.tag == 'config':
                result = HttpEndpointComunicator.send_config(xml_tree)
                response = XMLResponseTranslator.translate_xml_response_config(result.content)
                context = {'process_file_config_active': 'is-selected',
                           'is_active': 'active okay',
                           'message': 'Send XML file configuration to backend ʕ•́ᴥ•̀ʔっ',
                           'response_msg': response,
                           'response_active': 'response-active',
                           'load_file_configuration_active': 'is-selected'}
            else:
                context = {'process_file_config_active': 'is-selected',
                           'is_active': 'active error',
                           'load_file_configuration_active': 'is-selected',
                           'response_active': 'response-not-active',
                           'message': 'The XML file format is not as expected ( ˘︹˘ )'}
        except Exception as e:
            print(e)
            context = {'process_file_config_active': 'is-selected',
                       'is_active': 'active error',
                       'load_file_configuration_active': 'is-selected',
                       'response_active': 'response-not-active',
                       'message': f'The file could not be sent because the XML file could not be parsed.\n'
                                  'Please check the file format and try again ( ˘︹˘ )'}
    return render(request, 'load_file_configuration.html', context)


def process_file_transactions(request):
    context = {}
    if request.method == 'POST' and request.FILES['xml_file']:
        try:
            file = request.FILES['xml_file']
            data = file.read().decode('utf-8')
            xml_tree = ET.fromstring(data)
            if xml_tree.tag == 'transacciones':
                result = HttpEndpointComunicator.send_transactions(xml_tree)
                response = XMLResponseTranslator.translate_xml_response_config(result.content)
                context = {'process_file_config_active': 'is-selected',
                           'is_active': 'active okay',
                           'message': 'Send XML file configuration to backend ʕ•́ᴥ•̀ʔっ',
                           'response_msg': response,
                           'response_active': 'response-active',
                           'load_file_configuration_active': 'is-selected'}
            else:
                context = {'process_file_config_active': 'is-selected',
                           'is_active': 'active error',
                           'load_file_configuration_active': 'is-selected',
                           'response_active': 'response-not-active',
                           'message': 'The XML file format is not as expected ( ˘︹˘ )'}
        except Exception as e:
            print(e)
            context = {'process_file_config_active': 'is-selected',
                       'is_active': 'active error',
                       'load_file_configuration_active': 'is-selected',
                       'response_active': 'response-not-active',
                       'message': f'The file could not be sent because the XML file could not be parsed.\n'
                                  'Please check the file format and try again ( ˘︹˘ )'}
    return render(request, 'load_file_transactions.html', context)
