import mysql.connector

# conexão
conexao = mysql.connector.connect(
    host="localhost",        
    user="root",
    password="081106",
    database="sistema_votacao"
)

cursor = conexao.cursor()