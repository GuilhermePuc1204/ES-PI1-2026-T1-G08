from datetime import datetime
from database.conexao import conexao, cursor
from utils.criptografia import criptografar_cpf, criptografar_chave_acesso
from utils.auditoria import registrar_evento


def encerrar_votacao():
    """
    Executa o fluxo completo de encerramento da votação com autenticação do mesário.

    Fluxo:
        1. Autentica o mesário (título + 4 dígitos do CPF + chave de acesso)
        2. Solicita confirmação de encerramento
        3. Solicita a chave de acesso novamente como dupla confirmação
        4. Registra o encerramento no banco e no log

    Args:
        Nenhum.

    Returns:
        bool: True se a votação foi encerrada com sucesso, False caso contrário.
    """
    print("\n=== ENCERRAMENTO DA VOTAÇÃO ===")

    # Passo 1: Autenticação do mesário (RF002.01.07.01)
    titulo = input("Título de eleitor do mesário: ").strip()

    cursor.execute(
        "SELECT id, nome, cpf, mesario, chave_acesso FROM eleitores WHERE titulo_eleitor = %s",
        (titulo,)
    )
    eleitor = cursor.fetchone()

    # Verifica se o eleitor existe (RF002.01.07.02)
    if not eleitor:
        print("Mesário não encontrado.")
        registrar_evento("ALERTA", "Tentativa de acesso negado")
        return False

    id_eleitor, nome, cpf_criptografado, mesario, chave_armazenada = eleitor

    # Verifica se o eleitor tem perfil de mesário
    if not mesario:
        print("Eleitor não é mesário.")
        registrar_evento("ALERTA", "Tentativa de acesso negado")
        return False

    # Valida os 4 primeiros dígitos do CPF
    primeiros_digitos = input("4 primeiros dígitos do CPF: ").strip()
    if len(primeiros_digitos) != 4 or not primeiros_digitos.isdigit():
        print("Entrada inválida.")
        registrar_evento("ALERTA", "Tentativa de acesso negado")
        return False

    if criptografar_cpf(primeiros_digitos) != cpf_criptografado[:4]:
        print("Autenticação falhou.")
        registrar_evento("ALERTA", "Tentativa de acesso negado")
        return False

    # Valida a chave de acesso
    chave = input("Chave de acesso: ").strip()
    if criptografar_chave_acesso(chave) != chave_armazenada:
        print("Chave de acesso incorreta.")
        registrar_evento("ALERTA", "Tentativa de acesso negado")
        return False

    print(f"\nMesário autenticado: {nome}")

    # Passo 2: Confirmação de encerramento (RF002.01.07.03)
    confirmacao = input("\nDeseja realmente encerrar a votação? (s/n): ").strip().lower()

    # Se não confirmar, cancela e retorna ao menu da urna (RF002.01.07.04)
    if confirmacao != "s":
        print("Encerramento cancelado.")
        return False

    # Passo 3: Dupla confirmação com a chave de acesso (RF002.01.07.05)
    chave_dupla = input("Digite sua chave de acesso novamente para confirmar: ").strip()

    if criptografar_chave_acesso(chave_dupla) != chave_armazenada:
        print("Chave incorreta. Encerramento cancelado.")
        registrar_evento("ALERTA", "Tentativa de acesso negado")
        return False

    # Passo 4: Encerramento definitivo (RF002.01.07.06)
    agora = datetime.now()

    # Atualiza o status da urna para encerrada no banco de dados
    cursor.execute(
        "UPDATE urna SET status = %s, data_encerramento = %s ORDER BY id DESC LIMIT 1",
        ("encerrada", agora)
    )
    conexao.commit()

    # Registra o encerramento no log de auditoria (RF002.02.01.07)
    registrar_evento("ENCERRAMENTO", "Votação finalizada com sucesso.")

    print(f"\nVotação encerrada em {agora.strftime('%d/%m/%Y %H:%M:%S')}.")
    return True
