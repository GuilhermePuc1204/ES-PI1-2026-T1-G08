from datetime import datetime
import os
from database.conexao import cursor

PASTA_AUDITORIA = "./logs"
NOME_ARQUIVO_AUDITORIA = datetime.now().strftime("auditoria_%Y%m%d_%H%M%S_%f.txt")
ARQUIVO_AUDITORIA = os.path.join(PASTA_AUDITORIA, NOME_ARQUIVO_AUDITORIA)

def registrar_evento(acao, descricao):
    if not os.path.exists(PASTA_AUDITORIA):
        os.mkdir(PASTA_AUDITORIA)

    # Obtém data e hora atual
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Abre o arquivo em modo de escrita com acréscimo (append)
    arquivo = open(ARQUIVO_AUDITORIA, "a", encoding="utf-8")

    # Escreve uma linha no arquivo
    arquivo.write(data_hora + " | " + acao + " | " + descricao + "\n")

    # Fecha o arquivo
    arquivo.close()

def visualizar_auditoria():
    
    registrar_evento(
        "AUDITORIA_ACESSADA",
        "Auditoria visualizada"
    )

    print("\n=== AUDITORIA DO SISTEMA ===")

    try:
        arquivo = open(ARQUIVO_AUDITORIA, "r", encoding="utf-8")
    except FileNotFoundError:
        print("Nenhum registro de auditoria encontrado.")
        return

    linhas = arquivo.readlines()
    arquivo.close()

    if len(linhas) == 0:
        print("Nenhum registro de auditoria encontrado.")
        return

    for linha in linhas:
        print(linha.strip())


def listar_protocolos():
    print("\n=== PROTOCOLOS DE VOTAÇÃO ===")

    cursor.execute(
        "SELECT protocolo, data_hora FROM votos ORDER BY protocolo"
    )
    protocolos = cursor.fetchall()

    if not protocolos:
        print("Nenhum protocolo registrado.")
        return

    for p in protocolos:
        print(f"{p[0]} - {p[1]}")

    registrar_evento(
        "PROTOCOLOS_EXIBIDOS",
        "Protocolos de votação exibidos"
    )