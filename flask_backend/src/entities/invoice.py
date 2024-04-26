from datetime import datetime


class Invoice:
    def __init__(self, invoice_id, customer_nit, date, amount):
        self.__id = invoice_id
        self.__customer_nit = customer_nit
        self.__date = date
        self.__amount: float = amount

    @property
    def id(self):
        return self.__id

    @property
    def customer_nit(self):
        return self.__customer_nit

    @property
    def date(self):
        return self.__date

    @property
    def amount(self):
        return self.__amount

    @id.setter
    def id(self, invoice_id):
        self.__id = invoice_id

    @customer_nit.setter
    def customer_nit(self, customer_nit):
        self.__customer_nit = customer_nit

    @date.setter
    def date(self, date):
        self.__date = date

    @amount.setter
    def amount(self, amount):
        self.__amount = float(amount)

    def to_datetime(self):
        invoice_date = datetime.strptime(self.date, "%d/%m/%Y").date()
        return invoice_date.strftime("%d/%m/%Y")

    def __str__(self):
        return (f"invoice_id: {self.id}, "
                f"customer_nit: {self.customer_nit}, "
                f"date: {self.date}, "
                f"amount: {self.amount}")
