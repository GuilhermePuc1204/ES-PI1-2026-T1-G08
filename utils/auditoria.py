from datetime import datetime

ARQUIVO_AUDITORIA = "./logs/log.txt"

def registrar_evento(acao, descricao):
    """
    Registra um evento de auditoria em arquivo texto.

    Parâmetros:
    acao (str)       -> Tipo do evento (ex: ABERTURA_URNA)
    descricao (str)  -> Descrição do evento
    """
    

    # Obtém data e hora atual
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Abre o arquivo em modo de escrita com acréscimo (append)
    arquivo = open(ARQUIVO_AUDITORIA, "a", encoding="utf-8")

    # Escreve uma linha no arquivo
    arquivo.write(data_hora + " | " + acao + " | " + descricao + "\n")

    # Fecha o arquivo
    arquivo.close()


def visualizar_auditoria():
    """
    Exibe todos os registros de auditoria salvos no arquivo.
    """

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