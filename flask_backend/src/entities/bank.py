class Bank:
    def __init__(self, code, name):
        self.__code = code
        self.__name = name

    @property
    def code(self):
        return self.__code

    @code.setter
    def code(self, code):
        self.__code = code

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    def __str__(self):
        return f'code: {self.code}, name: {self.name}'
