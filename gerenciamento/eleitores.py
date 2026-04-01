import random
from database.conexao import conexao, cursor


def gerar_chave(nome):
    partes = nome.upper().split()

    if len(partes) < 2:
        return None

    return partes[0][:2] + partes[1][0] + str(random.randint(1000, 9999))


def cadastrar_eleitor():
    print("\n=== CADASTRO DE ELEITOR ===")

    nome = input("Nome completo: ")
    cpf = input("CPF: ")
    titulo = input("Título de eleitor: ")
    mesario = input("É mesário? (s/n): ").lower() == "s"

    # verifica duplicidade
    sql = "SELECT * FROM eleitores WHERE cpf = %s OR titulo_eleitor = %s"
    cursor.execute(sql, (cpf, titulo))

    if cursor.fetchone():
        print("CPF ou título já cadastrado.")
        return

    chave = gerar_chave(nome)

    if not chave:
        print("Nome inválido.")
        return

    sql = """
    INSERT INTO eleitores (nome, cpf, titulo_eleitor, mesario, chave_acesso)
    VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(sql, (nome, cpf, titulo, mesario, chave))
    conexao.commit()

    print("\nEleitor cadastrado com sucesso!")
    print("Chave:", chave)


def listar_eleitores():
    print("\n=== LISTA DE ELEITORES ===")

    sql = "SELECT nome, cpf, titulo_eleitor, mesario, status_voto FROM eleitores"
    cursor.execute(sql)

    dados = cursor.fetchall()

    if not dados:
        print("Nenhum eleitor cadastrado.")
        return

    for e in dados:
        print("\n------------------")
        print("Nome:", e[0])
        print("CPF:", e[1])
        print("Título:", e[2])
        print("Mesário:", "Sim" if e[3] else "Não")
        print("Status:", e[4])


def buscar_eleitor():
    print("\n=== BUSCAR ELEITOR ===")

    valor = input("CPF ou Título: ")

    sql = """
    SELECT nome, cpf, titulo_eleitor, mesario, status_voto
    FROM eleitores
    WHERE cpf = %s OR titulo_eleitor = %s
    """

    cursor.execute(sql, (valor, valor))
    e = cursor.fetchone()

    if not e:
        print("Eleitor não encontrado.")
        return

    print("\n=== ENCONTRADO ===")
    print("Nome:", e[0])
    print("CPF:", e[1])
    print("Título:", e[2])
    print("Mesário:", "Sim" if e[3] else "Não")
    print("Status:", e[4])


def remover_eleitor():
    print("\n=== REMOVER ELEITOR ===")

    cpf = input("CPF: ")

    sql = "SELECT * FROM eleitores WHERE cpf = %s"
    cursor.execute(sql, (cpf,))

    if not cursor.fetchone():
        print("Eleitor não encontrado.")
        return

    confirm = input("Confirmar remoção? (s/n): ")

    if confirm != "s":
        return

    sql = "DELETE FROM eleitores WHERE cpf = %s"
    cursor.execute(sql, (cpf,))
    conexao.commit()

    print("Removido com sucesso.")