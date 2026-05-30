import os
from datetime import datetime
from database.conexao import cursor
from utils.descriptografia import descriptografar_protocolo


PASTA_AUDITORIA = "./logs"
NOME_ARQUIVO_AUDITORIA = datetime.now().strftime("auditoria_%Y%m%d_%H%M%S_%f.txt")
ARQUIVO_AUDITORIA = os.path.join(PASTA_AUDITORIA, NOME_ARQUIVO_AUDITORIA)

def registrar_evento(acao, descricao):
    """
    Registra um evento no arquivo de log de auditoria do sistema.

    Cria a pasta de logs caso ainda não exista e adiciona uma nova linha
    ao arquivo de auditoria com o timestamp atual, o tipo da ação e a
    descrição do evento, no formato:
    [YYYY/MM/DD HH:MM:SS] ACAO | descricao

    Args:
        acao (str): Tipo da ocorrência (ex: "ABERTURA", "ALERTA",
            "SUCESSO", "ENCERRAMENTO").
        descricao (str): Descrição detalhada do evento registrado.

    Returns:
        None: A função não retorna valor; o efeito é a gravação em
        arquivo.
    """
    if not os.path.exists(PASTA_AUDITORIA):
        os.mkdir(PASTA_AUDITORIA)

    # Obtém data e hora atual
    data_hora = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    # Abre o arquivo em modo de escrita com acréscimo (append)
    arquivo = open(ARQUIVO_AUDITORIA, "a", encoding="utf-8")

    # Escreve uma linha no arquivo
    arquivo.write(f"[{data_hora}] {acao} | {descricao}\n")

    # Fecha o arquivo
    arquivo.close()

def visualizar_auditoria():
    """
    Lê e exibe no terminal o conteúdo do arquivo de auditoria atual.

    Abre o arquivo de logs gerado na execução corrente e imprime cada
    linha registrada, permitindo a conferência das ocorrências.
    Caso o arquivo não exista ou esteja vazio, informa o usuário.

    Args:
        Nenhum.

    Returns:
        None: A função apenas imprime no terminal.
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


def listar_protocolos():
    """
    Lista todos os protocolos de votação registrados no banco de dados.

    Consulta a tabela de votos, descriptografa cada protocolo armazenado
    (que está cifrado com a Cifra de Hill) e exibe no terminal o
    protocolo original junto com a data e hora do voto, em ordem
    alfabética.

    Args:
        Nenhum.

    Returns:
        None: A função apenas imprime no terminal.
    """
    print("\n=== PROTOCOLOS DE VOTAÇÃO ===")

    cursor.execute(
        "SELECT protocolo, data_hora FROM votos ORDER BY protocolo"
    )
    protocolos = cursor.fetchall()

    if not protocolos:
        print("Nenhum protocolo registrado.")
        return

    for p in protocolos:
        protocolo_cifrado = p[0]
        data_hora = p[1]

        protocolo_original = descriptografar_protocolo(protocolo_cifrado)

        print(f"{protocolo_original} - {data_hora}")