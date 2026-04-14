"""
Módulo: eleitores.py

Responsabilidade:
Este módulo implementa todas as funcionalidades do Módulo de Gerenciamento
relacionadas aos eleitores, conforme os requisitos RF001 do projeto.

Funções principais:
- Cadastro de eleitores com validação, unicidade e criptografia
- Listagem de eleitores cadastrados
- Busca de eleitor por CPF ou Título
- Remoção de eleitor

Aspectos de segurança:
- CPF e chave de acesso são criptografados antes de serem persistidos (RNF006)
- Nenhuma informação sensível é armazenada em texto claro no banco de dados
"""

import random  # Utilizado para geração de números aleatórios na chave de acesso
import re      # Utilizado para normalização de entradas (expressões regulares)

from database.conexao import conexao, cursor
from utils.validacoes import validar_cpf, validar_titulo_eleitor
from utils.criptografia import criptografar_cpf, criptografar_chave_acesso


# ==========================================================
# GERAÇÃO DA CHAVE DE ACESSO DO ELEITOR
# ==========================================================
def gerar_chave(nome):
    """
    Gera a chave de acesso do eleitor conforme especificação do projeto.

    Regra de formação:
    - 2 primeiras letras do primeiro nome
    - 1ª letra do segundo nome
    - 4 dígitos aleatórios

    Exemplo:
        Nome: André Silva
        Chave gerada: ANS4821

    Args:
        nome (str): Nome completo do eleitor.

    Returns:
        str | None: Chave gerada ou None caso o nome seja inválido.
    """

    # Converte o nome para maiúsculas e separa por espaços
    partes = nome.upper().split()

    # Exige pelo menos nome e sobrenome
    if len(partes) < 2:
        return None

    # Monta a chave conforme o padrão definido
    return partes[0][:2] + partes[1][0] + str(random.randint(1000, 9999))


# ==========================================================
# CADASTRO DE ELEITOR (RF001.01 / RF001.02 / RF001.03)
# ==========================================================
def cadastrar_eleitor():
    """
    Realiza o cadastro de um novo eleitor no sistema.

    Etapas do processo:
    1. Leitura dos dados de entrada
    2. Normalização dos documentos
    3. Validação matemática do CPF e do Título
    4. Criptografia do CPF
    5. Verificação de unicidade no banco
    6. Geração e criptografia da chave de acesso
    7. Inserção do eleitor no banco de dados
    """

    print("\n=== CADASTRO DE ELEITOR ===")

    # -----------------------------
    # ENTRADA DE DADOS
    # -----------------------------
    nome = input("Nome completo: ").strip()
    cpf = input("CPF: ").strip()
    titulo = input("Título de eleitor: ").strip()
    mesario = input("É mesário? (s/n): ").strip().lower() == "s"

    # -----------------------------
    # NORMALIZAÇÃO DOS DOCUMENTOS
    # Remove qualquer caractere que não seja numérico
    # -----------------------------
    cpf = re.sub(r"\D", "", cpf)
    titulo = re.sub(r"\D", "", titulo)

    # -----------------------------
    # VALIDAÇÃO MATEMÁTICA (RF001.02)
    # -----------------------------
    if not validar_cpf(cpf):
        print("CPF inválido.")
        return

    if not validar_titulo_eleitor(titulo):
        print("Título de eleitor inválido.")
        return

    # -----------------------------
    # CRIPTOGRAFIA DO CPF (RNF006)
    # -----------------------------
    cpf_criptografado = criptografar_cpf(cpf)

    # -----------------------------
    # VERIFICAÇÃO DE UNICIDADE (RF001.03)
    # Comparação feita com CPF já criptografado
    # -----------------------------
    sql = "SELECT 1 FROM eleitores WHERE cpf = %s OR titulo_eleitor = %s"
    cursor.execute(sql, (cpf_criptografado, titulo))

    if cursor.fetchone():
        print("CPF ou título já cadastrado.")
        return

    # -----------------------------
    # GERAÇÃO E CRIPTOGRAFIA DA CHAVE DE ACESSO
    # -----------------------------
    chave = gerar_chave(nome)

    if not chave:
        print("Nome inválido.")
        return

    chave_criptografada = criptografar_chave_acesso(chave)

    # -----------------------------
    # INSERÇÃO NO BANCO DE DADOS
    # -----------------------------
    sql = """
    INSERT INTO eleitores (nome, cpf, titulo_eleitor, mesario, chave_acesso)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(
        sql,
        (nome, cpf_criptografado, titulo, mesario, chave_criptografada)
    )
    conexao.commit()

    print("\nEleitor cadastrado com sucesso!")
    print("Chave de acesso (guarde):", chave)


# ==========================================================
# LISTAGEM DE ELEITORES (RF001.08)
# ==========================================================
def listar_eleitores():
    """
    Lista todos os eleitores cadastrados no sistema.

    Observação:
    - O CPF é exibido de forma criptografada, conforme requisitos de segurança.
    - A chave de acesso não é exibida por se tratar de dado sensível.
    """

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


# ==========================================================
# BUSCA DE ELEITOR (RF001.07)
# ==========================================================
def buscar_eleitor():
    """
    Busca um eleitor pelo CPF ou pelo Título de Eleitor.

    Regras:
    - Se a entrada possuir 11 dígitos, considera-se CPF
    - Caso contrário, considera-se Título de Eleitor
    """

    print("\n=== BUSCAR ELEITOR ===")

    valor = input("CPF ou Título: ").strip()
    somente_numeros = re.sub(r"\D", "", valor)

    if len(somente_numeros) == 11:
        cpf_criptografado = criptografar_cpf(somente_numeros)
        sql = """
        SELECT nome, cpf, titulo_eleitor, mesario, status_voto
        FROM eleitores
        WHERE cpf = %s
        """
        cursor.execute(sql, (cpf_criptografado,))
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


# ==========================================================
# REMOÇÃO DE ELEITOR (RF001.06)
# ==========================================================
def remover_eleitor():
    """
    Remove um eleitor do sistema a partir do CPF.

    O CPF informado é normalizado e criptografado antes
    de ser utilizado na consulta e remoção no banco.
    """

    print("\n=== REMOVER ELEITOR ===")

    cpf = input("CPF: ").strip()
    cpf_limpo = re.sub(r"\D", "", cpf)

    if len(cpf_limpo) != 11:
        print("CPF inválido.")
        return

    cpf_criptografado = criptografar_cpf(cpf_limpo)

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

    sql = "DELETE FROM eleitores WHERE cpf = %s"
    cursor.execute(sql, (cpf_criptografado,))
    conexao.commit()

    print("Eleitor removido com sucesso.")
