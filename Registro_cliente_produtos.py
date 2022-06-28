from numpy.lib.shape_base import column_stack
import pandas as pd
import os

# Função para exibição do menu

def menu():
    try:
        escolha = int(input("\n<1> Para registrar cliente: "
                            "\n<2> Salvar alterações: "
                            "\n<3> Exibir produtos dos clientes: "
                            "\n<4> Calcular a pontuação dos clientes"
                            "\n<5> Sair: \n"))
    except ValueError:
        print('\nOpção inválida, digite um numero de 1 a 5 !')
        return False
    else:
        return escolha

# Classes de erro

class numeroInvalido (Exception):
    pass
class campoVazio (Exception):
    pass
class cpfInvalido (Exception):
    pass

# Função para validação de CPF

def validacao_cpf(numeric):
    cpf_lista=[]
    cpf_string = str(numeric)
    for numero in cpf_string:
        cpf_lista.append(int(numero))
    if len(cpf_lista) == 11:
        verificacao_1 = 0
        for i in range (0,len(cpf_lista)-2):
            verificacao_1 = cpf_lista[i]*(10-i) + verificacao_1
        resto_1 = (verificacao_1*10)%11
        verificacao_2 = 0
        for i in range (0,len(cpf_lista)-1):
            verificacao_2 = cpf_lista[i]*(11-i) + verificacao_2
        resto_2=(verificacao_2*10)%11
        if resto_1 == 10:
            resto_1 = 0
        if resto_2 == 10:
            resto_2 = 0
        if resto_1 == cpf_lista[9] and resto_2 == cpf_lista[10]:
            return True
        else:
            return False
    else:
        return False

# Função para cadastro de produtos

def cadastrar_Produtos_Safra(numeric):

    if numeric == 1:
        lista_produtos_PF = ['Conta Corrente', 'Cartões', 'Crédito', 'Câmbio', 'Seguros']
        for i in range(0, len(lista_produtos_PF)):
            print(i+1, lista_produtos_PF[i])
        indice_produto = int(input("\nDigite o índice do produto que deseja adicionar: "))
        produto = lista_produtos_PF[indice_produto - 1]
        return produto
    elif numeric == 2:
        lista_produtos_PJ = ['Conta Corrente', 'Cash Management | Serviçis',
                             'Câmbio e Comércio Exterior', 'Empréstimos e Financiamentos', 'Seguros para Empresas']
        for i in range(0, len(lista_produtos_PJ)):
            print(i+1, lista_produtos_PJ[i])
        indice_produto = int(input("\nDigite o índice do produto que deseja adicionar: "))
        produto = lista_produtos_PJ[(indice_produto-1)]
        return produto

# Função para registro de clientes

def registrarCliente (dicionario):

    res ='S'
    while res == 'S' or res == 'SIM':
        produtos_safra = []
        try:
            nome = input("\nDigite o primeiro nome do Cliente: ").upper()
            sobrenome = input("\nDigite o sobrenome: ").upper()
            if nome == "" or sobrenome == "":
                raise campoVazio
            cpf = int(input('\nDigite o CPF com 11 dígitos: '))
            # Realizando a validação do CPF, primeiro em relação a quantidade de dígitos
            # Depois fazendo a validação pela função disponibilizada pela Ministério da Fazenda
            val = validacao_cpf(cpf)
            if val == False:
                raise cpfInvalido
            tipo_conta = int(input('\nDigite o índice do tipo de conta (1/2): '
                                   '\n1-Pessoa Física'
                                   '\n2-Pessoa Jurídica \n'))
            if tipo_conta < 1 or tipo_conta > 2:
                raise numeroInvalido
            conta = int(input("\nDigite a conta do cliente: "))
            res_1 = input("\nDeseja adicionar produtos do cliente? (S/N)") .upper()
            while res_1 == 'S' or res_1 == 'SIM':
                produto = cadastrar_Produtos_Safra(tipo_conta)
                produtos_safra.append(produto)
                print("\nProduto adicionado com sucesso! ")
                res_1 = input("\nDeseja adicionar outro produto? (S/N)").upper()
            dicionario[cpf] = [nome,sobrenome,conta,tipo_conta, produtos_safra]

        except numeroInvalido:
            print('\nDigite o número "1" para pessoa física ou "2" para pessoa jurídica ')

        except ValueError:
            print('\nO cliente não foi cadastrado ! Valor de entrada incorreto. '
                  'Lembrando que CPF, Conta e o tipo da conta são números inteiros! Os produtos também'
                  ' são adicionados pelo índice, portanto são números inteiros. ')
        except campoVazio:
            print('\nO campo do nome e sobrenome devem ser preechidos: ')
        except cpfInvalido:
            print('\nDigite um número de CPF válido com 11 dígitos: ')
        finally:
            res=input("\nDigite <S> para inserir um novo cliente.").upper()

# Função para salvar registro em arquivo CSV

def salvarRegistro(dicionario):

    with open("listaClientes_2.csv", "a") as inv:
        for chave, valor in dicionario.items():
                inv.write(str(chave) + ";" + str(valor[0]) + ";" +
                          str(valor[1]) + ";" + str(valor[2]) + ";" +
                          str(valor[3]) + ";" + str(valor[4]) + "\n")
    return print("\nSalvo com sucesso!")

# Função para exibir as informações do arquivo salvo

def exibir():

    try:
        with open("listaClientes_2.csv", "r") as inv:
            linhas = inv.readlines()
    except FileNotFoundError:
        print('\nNão existe cadastro de cliente no arquivo'
              '\nSalve o registro antes de realizar a consulta! ')
        return False
    else:
        return linhas

# Função para pontuar o cliente de acordo com os produtos 

            
def pontuar_cliente ():

    if os.path.exists("listaClientes_2.csv"):
        dicionario_produtos ={'Conta Corrente':6, 'Cartões':6, 'Crédito':7, 'Câmbio':8.5, 'Seguros':7.5,'Cash Management | Serviçis':5,
                    'Câmbio e Comércio Exterior':10, 'Empréstimos e Financiamentos':8, 'Seguros para Empresas':7}
        lista_clientes = pd.read_csv("listaClientes_2.csv", sep=";",encoding = 'latin1',
                                    names = ['cpf', 'nome', 'sobrenome','conta', 'tipo_conta', 'produtos'])
        lista_clientes['produtos'] = lista_clientes['produtos'].apply(lambda x: str(x).replace("[",""))
        lista_clientes['produtos'] = lista_clientes['produtos'].apply(lambda x: str(x).replace("]",""))
        lista_clientes['produtos'] = lista_clientes['produtos'].apply(lambda x: str(x).replace("'",""))   
        lista_produtos_tratados = lista_clientes['produtos']
        score_clientes = []
        
        for linha in lista_produtos_tratados:
            pontuacao_cliente = []
            lista_produtos = str(linha).split(",")        
            for produto in lista_produtos:
                produto_tratado = str.strip(produto) 
                for chave, valor in dicionario_produtos.items():
                    if produto_tratado == chave:
                        pontuacao_cliente.append(valor)
            score = (sum(pontuacao_cliente)/len(pontuacao_cliente))
            score_clientes.append(round(score,2))
        lista_clientes['pontuação'] = score_clientes
        print('\nPontuação dos clientes: ') 
        print(lista_clientes[['nome','sobrenome','produtos','pontuação']])  
    else:
        print("\nNão existe arquivo salvo com o nome de 'listaClientes_2.csv'. \nSalve o registro antes! ")
 
# Chamar a função de menu e iniciar a interação com o usuário 

opcao = menu()
registro = {}

if opcao == False:
    opcao = menu()

while opcao > 0 and opcao < 5:
    if opcao == 1:
        registrarCliente(registro)
    elif opcao == 2:
        salvarRegistro(registro)
    elif opcao == 3:
        resultado = exibir()
        if resultado == False:
            pass
        else:
            for linha in resultado:
                lista=linha.split(";")
                print("Cliente.........: ", lista[1], lista[2])
                print("Tipo de conta...: ", lista[4])
                print("Produtos.....: ", lista[5])
    elif opcao == 4:
        pontuar_cliente()

    opcao = menu()