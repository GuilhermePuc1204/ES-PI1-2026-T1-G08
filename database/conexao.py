import mysql.connector

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123@",  
    database="sistema_votacao"
)

cursor = conexao.cursor()