class Customer:
    def __init__(self, nit, name):
        self.__nit = nit
        self.__name = name

    @property
    def nit(self):
        return self.__nit

    @nit.setter
    def nit(self, nit):
        self.__nit = nit

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    def __str__(self):
        return f'nit: {self.nit}, name: {self.name}'
