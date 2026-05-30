import re
from datetime import datetime
from database.conexao import cursor
from utils.criptografia import criptografar_cpf, criptografar_chave_acesso
from utils.auditoria import registrar_evento


def encerrar_votacao():
    """
    Realiza o encerramento da votação com dupla confirmação do mesário.

    Solicita título, 4 primeiros dígitos do CPF e chave de acesso do
    mesário, valida o perfil, pede confirmação ("Deseja realmente
    encerrar a votação?") e, em caso afirmativo, exige uma segunda
    inserção da chave de acesso. Apenas se ambas as validações forem
    bem-sucedidas o encerramento é confirmado. Eventos de falha são
    registrados em log.

    Args:
        Nenhum (toda a entrada é coletada via input do terminal).

    Returns:
        bool: True se o encerramento foi confirmado com sucesso, False
        em qualquer falha de autenticação ou cancelamento pelo mesário.
    """
    print("\n=== ENCERRAMENTO DA VOTAÇÃO ===")

    # --- PASSO 1: IDENTIFICAÇÃO DO MESÁRIO PELO TÍTULO ---
    titulo = input("Título de eleitor do mesário: ").strip()
    titulo_limpo = re.sub(r"\D", "", titulo)

    if len(titulo_limpo) < 4:
        print("Digite pelo menos 4 números do título.")
        registrar_evento(
            "LOGIN_MESARIO_FALHA",
            "Título do mesário inválido no encerramento"
        )
        return False

    cursor.execute(
        "SELECT id, nome, cpf, titulo_eleitor, mesario, chave_acesso FROM eleitores"
    )
    eleitores = cursor.fetchall()

    encontrados = []

    for e in eleitores:
        id_eleitor, nome, cpf_criptografado, titulo_eleitor, mesario, chave_armazenada = e
        if titulo_eleitor.startswith(titulo_limpo[:4]):
            encontrados.append(e)

    if not encontrados:
        print("Mesário não encontrado.")
        registrar_evento(
            "LOGIN_MESARIO_FALHA",
            "Tentativa de encerramento com título inexistente"
        )
        return False

    if len(encontrados) > 1:
        print("Mais de um mesário encontrado. Use o título completo.")
        registrar_evento(
            "LOGIN_MESARIO_FALHA",
            "Tentativa de encerramento com título ambíguo"
        )
        return False

    id_eleitor, nome, cpf_criptografado, titulo_eleitor, mesario, chave_armazenada = encontrados[0]

    if not mesario:
        print("Eleitor não é mesário.")
        registrar_evento(
            "LOGIN_MESARIO_FALHA",
            "Tentativa de encerramento por eleitor não mesário"
        )
        return False

    # --- PASSO 2: CPF PARCIAL ---
    primeiros_digitos = input("4 primeiros dígitos do CPF: ").strip()

    if len(primeiros_digitos) != 4 or not primeiros_digitos.isdigit():
        print("Entrada inválida.")
        registrar_evento(
            "LOGIN_MESARIO_FALHA",
            "CPF parcial inválido no encerramento"
        )
        return False

    if criptografar_cpf(primeiros_digitos) != cpf_criptografado[:4]:
        print("Autenticação falhou.")
        registrar_evento(
            "LOGIN_MESARIO_FALHA",
            "CPF parcial incorreto no encerramento"
        )
        return False

    # --- PASSO 3: CHAVE DE ACESSO ---
    chave = input("Chave de acesso: ").strip()

    if criptografar_chave_acesso(chave) != chave_armazenada:
        print("Chave de acesso incorreta.")
        registrar_evento(
            "LOGIN_MESARIO_FALHA",
            "Chave incorreta no encerramento"
        )
        return False

    print(f"\nMesário autenticado: {nome}")

    # --- PASSO 4: CONFIRMAÇÃO ---
    confirmacao = input("\nDeseja realmente encerrar a votação? (s/n): ").strip().lower()
    if confirmacao != "s":
        print("Encerramento cancelado.")
        return False

    # --- PASSO 5: DUPLA CONFIRMAÇÃO ---
    chave_dupla = input("Digite sua chave de acesso novamente para confirmar: ").strip()

    if criptografar_chave_acesso(chave_dupla) != chave_armazenada:
        print("Chave incorreta. Encerramento cancelado.")

        return False

    registrar_evento(
        "ENCERRAMENTO",
        "Votação finalizada com sucesso"
    )
    agora = datetime.now()
    print(f"\nVotação encerrada em {agora.strftime('%d/%m/%Y %H:%M:%S')}.")
    return True
