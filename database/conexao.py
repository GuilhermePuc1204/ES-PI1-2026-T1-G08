import mysql.connector

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  
    database="sistema_votacao"
)

cursor = conexao.cursor()