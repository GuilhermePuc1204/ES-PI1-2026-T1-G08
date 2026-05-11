from database.conexao import conexao, cursor
from datetime import datetime
import random
import string
from utils.criptografia import criptografar_cpf, criptografar_chave_acesso


def gerar_protocolo(numero):
    letras = ''.join(random.choices(string.ascii_uppercase, k=2))
    numeros = ''.join(random.choices(string.digits, k=5))
    return f"V{letras}26{numero}{numeros}"


def votar():

    print("\n=== IDENTIFICAÇÃO DO ELEITOR ===")

    titulo = input("Título de eleitor: ").strip()
    cpf_input = input("CPF (somente números): ").strip()
    chave = input("Chave de acesso: ").strip()

    # busca eleitor
    cursor.execute(
        "SELECT id, cpf, chave_acesso, status_voto FROM eleitores WHERE titulo_eleitor = %s",
        (titulo,)
    )
    eleitor = cursor.fetchone()

    if not eleitor:
        print("Eleitor não encontrado.")
        return

    id_eleitor, cpf_criptografado, chave_armazenada, status = eleitor

    # valida CPF (comparando primeiros dígitos criptografados)
    if criptografar_cpf(cpf_input[:4]) != cpf_criptografado[:4]:
        print("CPF inválido.")
        return

    # valida chave
    if criptografar_chave_acesso(chave) != chave_armazenada:
        print("Chave incorreta.")
        return

    # verifica se já votou
    if status == "JA_VOTOU":
        print("Eleitor já votou.")
        return

    # votação
    numero = input("\nDigite o número do candidato: ").strip()

    cursor.execute(
        "SELECT id, nome, partido FROM candidatos WHERE numero = %s",
        (numero,)
    )
    candidato = cursor.fetchone()

    if candidato:
        print(f"\nNome: {candidato[1]}")
        print(f"Partido: {candidato[2]}")
    else:
        print("\nVOTO NULO")

    confirm = input("Confirmar voto? (s/n): ")

    if confirm.lower() != "s":
        print("Voto cancelado.")
        return

    protocolo = gerar_protocolo(numero)

    id_candidato = candidato[0] if candidato else None

    cursor.execute(
        "INSERT INTO votos (id_candidato, data_hora, protocolo) VALUES (%s, %s, %s)",
        (id_candidato, datetime.now(), protocolo)
    )

    cursor.execute(
        "UPDATE eleitores SET status_voto = 'JA_VOTOU' WHERE id = %s",
        (id_eleitor,)
    )

    conexao.commit()

    print("\nVoto registrado com sucesso!")
    print(f"Protocolo: {protocolo}")