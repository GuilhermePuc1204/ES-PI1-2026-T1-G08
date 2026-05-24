import os
from datetime import datetime

# Caminho do arquivo de log relativo à raiz do projeto
ARQUIVO_AUDITORIA = os.path.join(os.path.dirname(__file__), '..', 'logs', 'log.txt')


def registrar_evento(acao, descricao):
    """
    Registra um evento crítico no arquivo de log (.txt).

    O formato do registro segue o padrão exigido pelo RF002.02.01.02:
    [YYYY-MM-DD HH:MM:SS] ACAO: descricao

    Args:
        acao (str): Categoria do evento (ex: 'ABERTURA', 'ALERTA', 'SUCESSO', 'ENCERRAMENTO').
        descricao (str): Descrição detalhada do evento ocorrido.

    Returns:
        None
    """
    # Obtém data e hora atual no formato exigido pelo requisito
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Monta a linha de log no padrão [YYYY-MM-DD HH:MM:SS] ACAO: descricao
    linha = f"[{timestamp}] {acao}: {descricao}\n"

    # Abre o arquivo em modo append para não sobrescrever registros anteriores
    with open(ARQUIVO_AUDITORIA, "a", encoding="utf-8") as arquivo:
        arquivo.write(linha)


def visualizar_auditoria():
    """
    Lê e exibe o conteúdo completo do arquivo de log no terminal.

    Args:
        Nenhum.

    Returns:
        None
    """
    print("\n=== LOGS DE OCORRÊNCIAS ===")

    # Verifica se o arquivo existe antes de tentar abrir
    if not os.path.exists(ARQUIVO_AUDITORIA):
        print("Nenhum registro de auditoria encontrado.")
        return

    with open(ARQUIVO_AUDITORIA, "r", encoding="utf-8") as arquivo:
        linhas = arquivo.readlines()

    if not linhas:
        print("Nenhum registro de auditoria encontrado.")
        return

    for linha in linhas:
        print(linha.strip())