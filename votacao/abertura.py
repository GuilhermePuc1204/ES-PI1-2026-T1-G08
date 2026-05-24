import re
from datetime import datetime
from database.conexao import conexao, cursor
from utils.criptografia import criptografar_cpf, criptografar_chave_acesso
from utils.auditoria import registrar_evento
from votacao.urna import menu_urna


def abrir_votacao():
    print("\n=== ABERTURA DO SISTEMA DE VOTAÇÃO ===")

    titulo = input("Título de eleitor do mesário: ").strip()
    titulo_limpo = re.sub(r"\D", "", titulo)

    if len(titulo_limpo) < 4:
        print("Digite pelo menos 4 números do título.")
        registrar_evento(
            "LOGIN_MESARIO_FALHA",
            "Título do mesário informado com menos de 4 dígitos"
        )
        return

    # Busca todos os eleitores
    cursor.execute(
        "SELECT id, nome, cpf, titulo_eleitor, mesario, chave_acesso FROM eleitores"
    )
    eleitores = cursor.fetchall()

    encontrados = []

    # Filtra pelo prefixo do título
    for e in eleitores:
        id_eleitor, nome, cpf_criptografado, titulo_eleitor, mesario, chave_armazenada = e

        if titulo_eleitor.startswith(titulo_limpo[:4]):
            encontrados.append(e)

    if not encontrados:
        print("Mesário não encontrado.")
        registrar_evento(
            "LOGIN_MESARIO_FALHA",
            "Tentativa de abertura de urna com título inexistente"
        )
        return

    if len(encontrados) > 1:
        print("Mais de um mesário encontrado. Use o título completo.")
        registrar_evento(
            "LOGIN_MESARIO_FALHA",
            "Tentativa de abertura de urna com título ambíguo"
        )
        return

    # Apenas um eleitor encontrado
    id_eleitor, nome, cpf_criptografado, titulo_eleitor, mesario, chave_armazenada = encontrados[0]

    if not mesario:
        print("Eleitor não é mesário.")
        registrar_evento(
            "LOGIN_MESARIO_FALHA",
            "Tentativa de abertura de urna por eleitor não mesário"
        )
        return

    primeiros_digitos = input("4 primeiros dígitos do CPF: ").strip()

    if len(primeiros_digitos) != 4 or not primeiros_digitos.isdigit():
        print("Entrada inválida.")
        registrar_evento(
            "LOGIN_MESARIO_FALHA",
            "CPF parcial informado em formato inválido"
        )
        return

    if criptografar_cpf(primeiros_digitos) != cpf_criptografado[:4]:
        print("Autenticação falhou.")
        registrar_evento(
            "LOGIN_MESARIO_FALHA",
            "CPF parcial do mesário incorreto"
        )
        return

    chave = input("Chave de acesso: ").strip()

    if criptografar_chave_acesso(chave) != chave_armazenada:
        print("Chave incorreta.")
        registrar_evento(
            "LOGIN_MESARIO_FALHA",
            "Chave de acesso do mesário incorreta"
        )
        return

    print(f"\nMesário autenticado: {nome}")

    registrar_evento(
        "LOGIN_MESARIO",
        "Mesário autenticado com sucesso"
    )

    registrar_evento(
        "ABERTURA_URNA",
        "Urna aberta pelo mesário"
    )

    # --- ZERÉSIMA ---
    print("\n=== ZERÉSIMA ===")

    cursor.execute("DELETE FROM votos")
    cursor.execute("UPDATE eleitores SET status_voto = 'NAO_VOTOU'")
    conexao.commit()

    registrar_evento(
        "ZERESIMA",
        "Zerésima emitida com sucesso"
    )

    cursor.execute("SELECT nome, numero, partido FROM candidatos ORDER BY nome")
    candidatos = cursor.fetchall()

    if not candidatos:
        print("Nenhum candidato cadastrado.")
        return

    print("\nCandidatos com votos zerados:")
    for c in candidatos:
        print(f"{c[0]} - Nº {c[1]} ({c[2]}): 0 votos")

    print("\nSistema de votação aberto com sucesso!")

    menu_urna()