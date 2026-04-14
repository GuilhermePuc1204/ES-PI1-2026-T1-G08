import random  # importa o módulo random para gerar valores aleatórios
import re  # importa o módulo re para expressões regulares
from database.conexao import conexao, cursor  # importa a conexão e o cursor do banco para executar comandos SQL
from utils.validacoes import validar_cpf, validar_titulo_eleitor, validar_documentos  # importa as funções de validação de CPF e título de eleitor
from utils.criptografia import criptografar_cpf # Impporta a função de criptografia de cpf.
from utils.criptografia import criptografar_chave_acesso # Importa a função de criptografia da chave de acesso.

def gerar_chave(nome):  # função que gera uma chave de acesso com base no nome
    partes = nome.upper().split()  # transforma o nome em maiúsculo e separa em partes (por espaços)

    if len(partes) < 2:  # verifica se o nome tem pelo menos 2 partes (ex: nome e sobrenome)
        return None  # retorna None indicando que não é possível gerar a chave

    return partes[0][:2] + partes[1][0] + str(random.randint(1000, 9999))  # monta a chave: 2 letras do 1º nome + 1 letra do 2º + número aleatório


def cadastrar_eleitor():  # função para cadastrar um eleitor no sistema
    print("\n=== CADASTRO DE ELEITOR ===")  # mostra o título da tela de cadastro

    nome = input("Nome completo: ")  # lê o nome completo do eleitor
    cpf = input("CPF: ")  # lê o CPF do eleitor
    titulo = input("Título de eleitor: ")  # lê o título de eleitor
    mesario = input("É mesário? (s/n): ").lower() == "s"  # lê se é mesário e converte para boolean (True se for "s")

    
    #validação matematica
    if not validar_cpf(cpf):
        print("CPF inválido.") #Informa que o cpf não é válido.
        return #Sai da função sem cadastrar.
    
    if not validar_titulo_eleitor(titulo):
        print("Título de eleitor inválido.")# Informa que o título de eleitor não é válido.
        return #Sai da função sem cadastrar.

    #criptografia do cpf
    cpf_criptografado = criptografar_cpf(cpf) # Chama a função de criptografia do CPF e armazena o resultado.

    # verifica duplicidade
    sql = "SELECT * FROM eleitores WHERE cpf = %s OR titulo_eleitor = %s"  # comando SQL para verificar se CPF ou título já existem
    cursor.execute(sql, (cpf, titulo))  # executa o SELECT passando cpf e título como parâmetros

    if cursor.fetchone():  # se encontrou algum registro com o CPF ou título informado
        print("CPF ou título já cadastrado.")  # informa duplicidade
        return  # sai da função sem cadastrar

    chave = gerar_chave(nome)  # gera a chave de acesso a partir do nome

    if not chave:  # se a chave não foi gerada (ex: nome inválido)
        print("Nome inválido.")  # informa que o nome não permitiu gerar chave
        return  # sai da função
    
    
    # Criptografia da chave de acesso (RNF006)
    chave_criptografada = criptografar_chave_acesso(chave)


    sql = """  # comando SQL para inserir um novo eleitor
    INSERT INTO eleitores (nome, cpf, titulo_eleitor, mesario, chave_acesso)
    VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(sql, (nome, cpf_criptografado, titulo, mesario, chave_criptografada))  # executa o INSERT com os dados do eleitor
    conexao.commit()  # confirma a inserção no banco de dados

    print("\nEleitor cadastrado com sucesso!")  # mensagem de sucesso
    print("Chave:", chave)  # exibe a chave de acesso gerada


def listar_eleitores():
    print("\n=== LISTA DE ELEITORES ===")

    sql = """
    SELECT nome, cpf, titulo_eleitor, mesario, status_voto
    FROM eleitores
    """
    cursor.execute(sql)
    dados = cursor.fetchall()

    if not dados:
        print("Nenhum eleitor cadastrado.")
        return

    for e in dados:
        print("\n------------------")
        print("Nome:", e[0])
        print("CPF (criptografado):", e[1])
        print("Título:", e[2])
        print("Mesário:", "Sim" if e[3] else "Não")
        print("Status:", e[4])



def buscar_eleitor():
    print("\n=== BUSCAR ELEITOR ===")

    valor = input("CPF ou Título: ").strip()

    # Remove tudo que não é número
    somente_numeros = re.sub(r"\D", "", valor)

    # CASO 1: CPF (11 dígitos)
    if len(somente_numeros) == 11:
        cpf_criptografado = criptografar_cpf(somente_numeros)

        sql = """
        SELECT nome, cpf, titulo_eleitor, mesario, status_voto
        FROM eleitores
        WHERE cpf = %s
        """
        cursor.execute(sql, (cpf_criptografado,))


    # CASO 2: Título de eleitor
    else:
        sql = """
        SELECT nome, cpf, titulo_eleitor, mesario, status_voto
        FROM eleitores
        WHERE titulo_eleitor = %s
        """
        cursor.execute(sql, (somente_numeros,))

    e = cursor.fetchone()

    if not e:
        print("Eleitor não encontrado.")
        return

    print("\n=== ELEITOR ENCONTRADO ===")
    print("Nome:", e[0])
    print("CPF (criptografado):", e[1])
    print("Título:", e[2])
    print("Mesário:", "Sim" if e[3] else "Não")
    print("Status:", e[4])


def remover_eleitor():
    print("\n=== REMOVER ELEITOR ===")

    cpf = input("CPF: ").strip()

    # Limpa CPF (remove pontos, traços etc.)
    cpf_limpo = re.sub(r"\D", "", cpf)

    # Verificação básica
    if len(cpf_limpo) != 11:
        print("CPF inválido.")
        return

    # Criptografa para comparar com o banco
    cpf_criptografado = criptografar_cpf(cpf_limpo)

    # Verifica se existe
    sql = "SELECT nome FROM eleitores WHERE cpf = %s"
    cursor.execute(sql, (cpf_criptografado,))
    eleitor = cursor.fetchone()

    if not eleitor:
        print("Eleitor não encontrado.")
        return

    print(f"Eleitor encontrado: {eleitor[0]}")
    confirm = input("Confirmar remoção? (s/n): ").strip().lower()

    if confirm != "s":
        print("Remoção cancelada.")
        return

    # Remove do banco
    sql = "DELETE FROM eleitores WHERE cpf = %s"
    cursor.execute(sql, (cpf_criptografado,))
    conexao.commit()

    print("Eleitor removido com sucesso.")