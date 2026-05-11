from datetime import datetime
from database.conexao import conexao, cursor
from utils.criptografia import criptografar_cpf, criptografar_chave_acesso
from votacao.urna import menu_urna



def abrir_votacao():
    print("\n=== ABERTURA DO SISTEMA DE VOTAÇÃO ===")

    titulo = input("Título de eleitor do mesário: ").strip()

    cursor.execute(
        "SELECT id, nome, cpf, mesario, chave_acesso FROM eleitores WHERE titulo_eleitor = %s",
        (titulo,)
    )
    eleitor = cursor.fetchone()

    if not eleitor:
        print("Mesário não encontrado.")
        return

    id_eleitor, nome, cpf_criptografado, mesario, chave_armazenada = eleitor

    if not mesario:
        print("Eleitor não é mesário.")
        return

    primeiros_digitos = input("4 primeiros dígitos do CPF: ").strip()

    if len(primeiros_digitos) != 4 or not primeiros_digitos.isdigit():
        print("Entrada inválida.")
        return

    if criptografar_cpf(primeiros_digitos) != cpf_criptografado[:4]:
        print("Autenticação falhou.")
        return

    chave = input("Chave de acesso: ").strip()

    if criptografar_chave_acesso(chave) != chave_armazenada:
        print("Chave incorreta.")
        return

    print(f"\nMesário autenticado: {nome}")

    # --- ZERÉSIMA ---
    print("\n=== ZERÉSIMA ===")

    cursor.execute("DELETE FROM votos")
    cursor.execute("UPDATE eleitores SET status_voto = 'NAO_VOTOU'")
    conexao.commit()

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