from abc import ABC, abstractmethod

class Pessoa(ABC):
    def __init__(self, nome, telefone, email, endereco):
        self.__nome = nome
        self.__telefone = telefone
        self.__email = email
        self.__endereco = endereco



