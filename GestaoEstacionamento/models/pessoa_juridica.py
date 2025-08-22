from .pessoa import Pessoa

class PessoaJuridica(Pessoa):
    def __init__(self, nome, telefone, email, endereco, nome_empresa, cnpj):
        super().__init__(nome, telefone, email, endereco)
        self.__nome_empresa = nome_empresa
        self.__cnpj = cnpj

    @property
    def nome_empresa(self):
        return self.__nome_empresa

    @nome_empresa.setter
    def nome_empresa(self, nome_empresa):
        self.__nome_empresa = nome_empresa

    @property
    def cnpj(self):
        return self.__cnpj

    @cnpj.setter
    def cnpj(self, cnpj):
        self.__cnpj = cnpj