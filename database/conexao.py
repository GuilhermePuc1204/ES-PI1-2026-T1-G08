#Importa o módulo mysql.connector, que permite a conexão do python com o banco de dados sql
import mysql.connector

# conexão
#Aqui é onde são passadas as informações necessária para acessar o MySql
conexao = mysql.connector.connect(
    host="localhost",        # Endereço do servidor do banco
    user="root",             # Usuário do banco de dados
    password="081106",       # Senha do banco de dados
    database="sistema_votacao" # Nome do banco de dados que será utilizado
)


# Cria um cursor a partir da conexão
# O cursor é usado para executar comandos SQL (SELECT, INSERT, UPDATE, DELETE, etc.)
cursor = conexao.cursor()