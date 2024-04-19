from src.services.xml_db_service import XMLDBService
from src.utils import constants


class PaymentsDbService(XMLDBService):

    def __init__(self):
        super().__init__(constants.PATH_DB_PAYMENTS)

    def init_db(self):
        pass

    def append_child(self, child):
        pass

    def get_child_by_id(self, code):
        pass

    def is_entity_exist(self, code):
        pass