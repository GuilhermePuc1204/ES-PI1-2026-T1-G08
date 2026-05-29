import mysql.connector
from mysql.connector import Error

conexao = None
cursor = None


def conectar_banco():
    """
    Realiza a conexão com o banco de dados.
    Retorna True se conectar com sucesso, False caso contrário.
    """
    global conexao, cursor

    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
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