from datetime import datetime


class Payment:
    def __init__(self, bank_code, customer_nit, date, amount):
        self.__bank_code = bank_code
        self.__customer_nit = customer_nit
        self.__date = date
        self.__amount: float = amount

    @property
    def bank_code(self):
        return self.__bank_code

    @property
    def customer_nit(self):
        return self.__customer_nit

    @property
    def date(self):
        return self.__date

    @property
    def amount(self):
        return self.__amount

    @bank_code.setter
    def bank_code(self, bank_code):
        self.__bank_code = bank_code

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
        return (f'bank code: {self.bank_code}, '
                f'customer nit: {self.customer_nit}, '
                f'date: {self.date}, '
                f'amount: {self.amount}')
