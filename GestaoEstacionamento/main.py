from models.pessoa_fisica import PessoaFisica
from models.pessoa_juridica import PessoaJuridica

if __name__ == '__main__':

    print('Cadastro de pessoa física')
    nome = input('Nome: ')
    telefone = int(input('Telefone: '))
    data_nascimento = int(input('Data de nascimento: '))
    email = input('Email: ')
    endereco = input('Endereco: ')
    cpf = int(input('CPF: '))
    p_fisica = PessoaFisica(nome, telefone, email, endereco, data_nascimento, cpf)

    print('-'*30)
    print('Cadastro de pessoa juridica')
    nome = input('Nome: ')
    telefone = int(input('Telefone: '))
    email = input('Email: ')
    endereco = input('Endereco: ')
    nome_empresa = input('Nome da empresa: ')
    cnpj = int(input('CNPJ: '))
    p_juridica = PessoaJuridica(nome, telefone, email, endereco, nome_empresa, cnpj)

    print('-'*30)
    print(p_fisica.__dict__)
    print(p_juridica.__dict__)

