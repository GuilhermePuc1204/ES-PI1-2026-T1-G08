import random  
import re  
from database.conexao import conexao, cursor  
from utils.validacoes import validar_cpf, validar_titulo_eleitor  
from utils.criptografia import criptografar_cpf, criptografar_chave_acesso 
from utils.descriptografia import descriptografar_cpf
from utils.auditoria import registrar_evento

def gerar_chave(nome): 
    partes = nome.upper().split()  

    if len(partes) < 2:  # verifica se o nome tem pelo menos 2 partes (ex: nome e sobrenome)
        return None  

    return partes[0][:2] + partes[1][0] + str(random.randint(1000, 9999))  # monta a chave: 2 letras do 1º nome + 1 letra do 2º + número aleatório


def cadastrar_eleitor():  
    print("\n=== CADASTRO DE ELEITOR ===")  

    nome = input("Nome completo: ")  # lê o nome do eleitor

    cpf = input("CPF: ")  # lê o CPF do eleitor
    if not validar_cpf(cpf):
        print("CPF inválido.")
        return

    print("CPF válido.")

    titulo = input("Título de eleitor: ")  # lê o título de eleitor
    if not validar_titulo_eleitor(titulo):
        print("Título de eleitor inválido.")
        return

    print("Título de eleitor válido.")

    mesario = input("É mesário? (s/n): ").lower() == "s"  # lê se é mesário e converte para boolean (True se for "s")

    #criptografia do cpf
    cpf_criptografado = criptografar_cpf(cpf) 

    # verifica duplicidade
    sql = "SELECT * FROM eleitores WHERE cpf = %s OR titulo_eleitor = %s" 
    cursor.execute(sql, (cpf, titulo))  

    if cursor.fetchone(): 
        print("CPF ou título já cadastrado.")  # informa duplicidade
        return  # sai da função sem cadastrar

    chave = gerar_chave(nome)  

    if not chave:  
        print("Nome inválido.") 
        return  
    
    
    
    chave_criptografada = criptografar_chave_acesso(chave)


    sql = """  # comando SQL para inserir um novo eleitor
    INSERT INTO eleitores (nome, cpf, titulo_eleitor, mesario, chave_acesso)
    VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(sql, (nome, cpf_criptografado, titulo, mesario, chave_criptografada))  # executa o INSERT com os dados do eleitor
    conexao.commit()  # confirma a inserção no banco de dados

    print("\nEleitor cadastrado com sucesso!")  # mensagem de sucesso
    print("Chave:", chave)  # exibe a chave de acesso gerada
    
    registrar_evento(
        "CADASTRO_ELEITOR",
        "Eleitor cadastrado com sucesso"
    )


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
        cpf_original = descriptografar_cpf(e[1])
        cpf_formatado = ( f"{cpf_original[0:3]}."f"{cpf_original[3:6]}."f"{cpf_original[6:9]}-"f"{cpf_original[9:11]}")

        print("\n------------------")
        print("Nome:", e[0])
        print("CPF: ", cpf_formatado)
        print("Título:", e[2])
        print("Mesário:", "Sim" if e[3] else "Não")
        print("Status:", e[4])



def buscar_eleitor():
    print("\n=== BUSCAR ELEITOR ===")

    valor = input("Digite CPF ou Título: ").strip()

    somente_numeros = re.sub(r"\D", "", valor)

    if len(somente_numeros) < 4:
        print("Digite pelo menos 4 números.")
        return

    cursor.execute(
        "SELECT nome, cpf, titulo_eleitor, mesario, status_voto FROM eleitores"
    )
    eleitores = cursor.fetchall()

    cpf_prefixo_criptografado = criptografar_cpf(somente_numeros[:4])

    for e in eleitores:
        cpf_criptografado = e[1]

        # compara prefixo criptografado
        if cpf_criptografado.startswith(cpf_prefixo_criptografado):
            cpf_original = descriptografar_cpf(cpf_criptografado)
            cpf_formatado = (
                f"{cpf_original[:3]}."
                f"{cpf_original[3:6]}."
                f"{cpf_original[6:9]}-"
                f"{cpf_original[9:11]}"
            )

            print("\n=== ELEITOR ENCONTRADO ===")
            print("Nome:", e[0])
            print("CPF:", cpf_formatado)
            print("Título:", e[2])
            print("Mesário:", "Sim" if e[3] else "Não")
            print("Status:", e[4])
            return


    cursor.execute(
        """
        SELECT nome, cpf, titulo_eleitor, mesario, status_voto
        FROM eleitores
        WHERE titulo_eleitor LIKE %s
        """,
        (somente_numeros + "%",)
    )
    e = cursor.fetchone()

    if e:
        cpf_original = descriptografar_cpf(e[1])
        cpf_formatado = (
            f"{cpf_original[:3]}."
            f"{cpf_original[3:6]}."
            f"{cpf_original[6:9]}-"
            f"{cpf_original[9:11]}"
        )

        print("\n=== ELEITOR ENCONTRADO ===")
        print("Nome:", e[0])
        print("CPF:", cpf_formatado)
        print("Título:", e[2])
        print("Mesário:", "Sim" if e[3] else "Não")
        print("Status:", e[4])
        return

    print("Eleitor não encontrado.")

def remover_eleitor():
    print("\n=== REMOVER ELEITOR ===")

    cpf = input("Digite o CPF: ").strip()
    cpf_limpo = re.sub(r"\D", "", cpf)

    if len(cpf_limpo) < 4:
        print("Digite pelo menos 4 números do CPF.")
        return

    # Criptografa apenas os 4 primeiros dígitos
    prefixo_criptografado = criptografar_cpf(cpf_limpo[:4])

    # Busca todos os eleitores
    cursor.execute(
        "SELECT id, nome, cpf FROM eleitores"
    )
    eleitores = cursor.fetchall()

    encontrados = []

    # Filtra eleitores pelo prefixo do CPF criptografado
    for e in eleitores:
        id_eleitor, nome, cpf_criptografado = e

        if cpf_criptografado.startswith(prefixo_criptografado):
            encontrados.append(e)

    if not encontrados:
        print("Nenhum eleitor encontrado com esse CPF.")
        return

    if len(encontrados) > 1:
        print("\nMais de um eleitor encontrado. Remoção cancelada.")
        print("Eleitores encontrados:")

        for e in encontrados:
            print(f"- {e[1]}")

        print("Use o CPF completo para remover.")
        return

    # Apenas um eleitor encontrado
    id_eleitor, nome, cpf_criptografado = encontrados[0]

    print(f"\nEleitor encontrado: {nome}")
    confirm = input("Confirmar remoção? (s/n): ").strip().lower()

    if confirm != "s":
        print("Remoção cancelada.")
        return

    # Remove o eleitor
    cursor.execute(
        "DELETE FROM eleitores WHERE id = %s",
        (id_eleitor,)
    )
    conexao.commit()

    print("Eleitor removido com sucesso.")