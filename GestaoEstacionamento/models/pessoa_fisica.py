from .pessoa import Pessoa

class PessoaFisica(Pessoa):
    def __init__(self, nome, telefone, email, endereco, data_nascimento, cpf):
        super().__init__(nome, telefone, email, endereco)
        self.__data_nascimento = data_nascimento
        self.__cpf = cpf

    @property
    def data_nascimento(self):
        return self.__data_nascimento

    @data_nascimento.setter
    def data_nascimento(self, data_nascimento):
        self.__data_nascimento = data_nascimento

    @property
    def cpf(self):
        return self.__cpf

    @cpf.setter
    def cpf(self, cpf):
        self.__cpf = cpf

