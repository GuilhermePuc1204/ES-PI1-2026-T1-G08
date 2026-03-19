import random
#sem banco ate o momento
eleitores = []


def gerar_chave(nome):
    """
    Gera chave de acesso:
    2 letras do primeiro nome + 1 do segundo + 4 números
    """

    partes = nome.upper().split()

    if len(partes) < 2:
        return None

    chave = (
        partes[0][:2] +
        partes[1][0] +
        str(random.randint(1000, 9999))
    )

    return chave


def cpf_existe(cpf):
    for e in eleitores:
        if e["cpf"] == cpf:
            return True
    return False


def titulo_existe(titulo):
    for e in eleitores:
        if e["titulo"] == titulo:
            return True
    return False


def cadastrar_eleitor():
    
    print("\n=== CADASTRO DE ELEITOR ===")

    nome = input("Nome completo: ")
    cpf = input("CPF: ")
    titulo = input("Título de eleitor: ")
    mesario = input("É mesário? (s/n): ").lower() == "s"

    # duplicidade
    if cpf_existe(cpf):
        print("CPF já cadastrado.")
        return

    if titulo_existe(titulo):
        print("Título já cadastrado.")
        return

    # gerar chave
    chave = gerar_chave(nome)

    if not chave:
        print("Erro ao gerar chave. Nome inválido.")
        return

    eleitor = {
        "nome": nome,
        "cpf": cpf,
        "titulo": titulo,
        "mesario": mesario,
        "chave": chave,
        "status": "NAO_VOTOU"
    }

    eleitores.append(eleitor)

    print("\nEleitor cadastrado com sucesso!")
    print("Chave de acesso:", chave)