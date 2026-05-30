import mysql.connector
from mysql.connector import Error

conexao = None
cursor = None


def conectar_banco():
    """
    Estabelece a conexão com o banco de dados MySQL do sistema de votação.

    Atribui os objetos de conexão e cursor às variáveis globais do módulo,
    que são utilizadas pelas demais funções do projeto para executar
    queries.

    Args:
        Nenhum.

    Returns:
        bool: True se a conexão foi estabelecida com sucesso, False caso
        ocorra erro de conexão (ex: MySQL desligado, credenciais inválidas).
    """
    global conexao, cursor

    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="sistema_votacao"
        )

        cursor = conexao.cursor()
        return True

    except Error as e:
        print("\nERRO AO CONECTAR AO BANCO DE DADOS")
        print("Verifique se o MySQL está ativo.")
        print("Detalhes:", e)
        conexao = None
        cursor = None
        return False


# tenta conectar ao carregar o módulo
conectar_banco()