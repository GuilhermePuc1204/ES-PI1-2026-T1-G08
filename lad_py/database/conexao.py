import mysql.connector


def conectar():
    """
    Realiza a conexão com o banco de dados MySQL utilizado pelo sistema
    de votação da urna eletrônica.

    Args:
        None

    Returns:
        connection: objeto de conexão com o banco de dados se a conexão
        for realizada com sucesso. Caso ocorra erro, retorna None.
    """

    try:
        # cria conexão com o banco MySQL
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root123@",
            database="urna_eletronica"
        )

        return conexao

    except Exception as erro:
        print("Erro ao conectar ao banco:", erro)
        return None