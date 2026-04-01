import random  # importa o módulo random para gerar valores aleatórios
from database.conexao import conexao, cursor  # importa a conexão e o cursor do banco para executar comandos SQL


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

    sql = """  # comando SQL para inserir um novo eleitor
    INSERT INTO eleitores (nome, cpf, titulo_eleitor, mesario, chave_acesso)
    VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(sql, (nome, cpf, titulo, mesario, chave))  # executa o INSERT com os dados do eleitor
    conexao.commit()  # confirma a inserção no banco de dados

    print("\nEleitor cadastrado com sucesso!")  # mensagem de sucesso
    print("Chave:", chave)  # exibe a chave de acesso gerada


def listar_eleitores():  # função para listar todos os eleitores cadastrados
    print("\n=== LISTA DE ELEITORES ===")  # mostra o título da listagem

    sql = "SELECT nome, cpf, titulo_eleitor, mesario, status_voto FROM eleitores"  # comando SQL para buscar dados dos eleitores
    cursor.execute(sql)  # executa o SELECT

    dados = cursor.fetchall()  # busca todos os registros retornados

    if not dados:  # se não houver registros
        print("Nenhum eleitor cadastrado.")  # informa que não há eleitores
        return  # sai da função

    for e in dados:  # percorre cada eleitor retornado
        print("\n------------------")  # separador visual
        print("Nome:", e[0])  # imprime o nome
        print("CPF:", e[1])  # imprime o CPF
        print("Título:", e[2])  # imprime o título de eleitor
        print("Mesário:", "Sim" if e[3] else "Não")  # imprime "Sim" ou "Não" dependendo do boolean mesario
        print("Status:", e[4])  # imprime o status do voto


def buscar_eleitor():  # função para buscar um eleitor pelo CPF ou título
    print("\n=== BUSCAR ELEITOR ===")  # mostra o título da busca

    valor = input("CPF ou Título: ")  # lê o valor que pode ser CPF ou título

    sql = """  # comando SQL para buscar eleitor pelo CPF ou pelo título
    SELECT nome, cpf, titulo_eleitor, mesario, status_voto
    FROM eleitores
    WHERE cpf = %s OR titulo_eleitor = %s
    """

    cursor.execute(sql, (valor, valor))  # executa o SELECT usando o mesmo valor para CPF ou título
    e = cursor.fetchone()  # busca um único registro encontrado

    if not e:  # se não encontrou nenhum eleitor
        print("Eleitor não encontrado.")  # informa que não existe
        return  # sai da função

    print("\n=== ENCONTRADO ===")  # título de encontrado
    print("Nome:", e[0])  # imprime o nome
    print("CPF:", e[1])  # imprime o CPF
    print("Título:", e[2])  # imprime o título
    print("Mesário:", "Sim" if e[3] else "Não")  # imprime se é mesário
    print("Status:", e[4])  # imprime o status do voto


def remover_eleitor():  # função para remover um eleitor do sistema
    print("\n=== REMOVER ELEITOR ===")  # mostra o título da remoção

    cpf = input("CPF: ")  # lê o CPF do eleitor a ser removido

    sql = "SELECT * FROM eleitores WHERE cpf = %s"  # comando SQL para verificar se existe eleitor com esse CPF
    cursor.execute(sql, (cpf,))  # executa o SELECT passando o CPF

    if not cursor.fetchone():  # se não encontrou eleitor com esse CPF
        print("Eleitor não encontrado.")  # informa que não existe
        return  # sai da função

    confirm = input("Confirmar remoção? (s/n): ")  # pede confirmação antes de remover

    if confirm != "s":  # se não confirmar com "s"
        return  # cancela a remoção

    sql = "DELETE FROM eleitores WHERE cpf = %s"  # comando SQL para deletar o eleitor pelo CPF
    cursor.execute(sql, (cpf,))  # executa o DELETE passando o CPF
    conexao.commit()  # confirma a remoção no banco

    print("Removido com sucesso.")  # mensagem de sucesso