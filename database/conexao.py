import mysql.connector


def conectar():
    """
    Conexao local para testes, futuramente será alterado para a outra conexão
    """

    try:
        conexao = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="root123@",   
            database="sistema_votacao"
        )

        return conexao

    except Exception as erro:
        print("Erro ao conectar:", erro)
        return None