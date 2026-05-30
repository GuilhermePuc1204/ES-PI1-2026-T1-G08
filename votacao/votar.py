from database.conexao import conexao, cursor
from datetime import datetime
import random
from utils.criptografia import criptografar_cpf, criptografar_chave_acesso, criptografar_protocolo
from utils.auditoria import registrar_evento


def gerar_protocolo(numero):
    letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numeros = "0123456789"

    parte_letras = ""
    for i in range(2):
        i = random.randint(0, len(letras) - 1)
        parte_letras += letras[i]

    parte_numeros = ""
    for i in range(5):
        i = random.randint(0, len(numeros) - 1)
        parte_numeros += numeros[i]

    return "V" + parte_letras + "26" + numero + parte_numeros

def votar():

    print("\n=== IDENTIFICAÇÃO DO ELEITOR ===")

    titulo = input("Título de eleitor: ").strip()
    cpf_input = input("4 primeiros dígitos do CPF: ").strip()
    chave = input("Chave de acesso: ").strip()

    if len(cpf_input) != 4 or not cpf_input.isdigit():
        print("Entrada inválida. Digite exatamente os 4 primeiros dígitos do CPF.")
        return

    cursor.execute(
        "SELECT id, cpf, chave_acesso, status_voto FROM eleitores WHERE titulo_eleitor = %s",
        (titulo,)
    )
    eleitor = cursor.fetchone()

    if not eleitor:
        print("Eleitor não encontrado.")
        return

    id_eleitor, cpf_criptografado, chave_armazenada, status = eleitor

    if criptografar_cpf(cpf_input) != cpf_criptografado[:4]:
        print("CPF inválido.")
        return

    if criptografar_chave_acesso(chave) != chave_armazenada:
        print("Chave incorreta.")
        return

    if status == "JA_VOTOU":
        print("Eleitor já votou.")
        registrar_evento(
            "ALERTA",
            "Tentativa de voto duplo"
        )
        return

    confirm = ""
    candidato = None
    numero = ""
    while confirm.lower() != "s":
        numero = input("\nDigite o número do candidato: ").strip()

        cursor.execute(
            "SELECT id, nome, partido FROM candidatos WHERE numero = %s",
            (numero,)
        )
        candidato = cursor.fetchone()

        if candidato:
            print(f"\nNome: {candidato[1]}")
            print(f"Número: {numero}")
            print(f"Partido: {candidato[2]}")
        else:
            print("\nVOTO NULO")

        confirm = input("Confirmar voto? (s/n): ")

    protocolo = gerar_protocolo(numero)
    protocolo_criptografado = criptografar_protocolo(protocolo)
    id_candidato = candidato[0] if candidato else None

    cursor.execute(
        "INSERT INTO votos (id_candidato, data_hora, protocolo) VALUES (%s, %s, %s)",
        (id_candidato, datetime.now(), protocolo_criptografado)
    )

    cursor.execute(
        "UPDATE eleitores SET status_voto = 'JA_VOTOU' WHERE id = %s",
        (id_eleitor,)
    )

    conexao.commit()

    registrar_evento(
        "SUCESSO",
        "Voto realizado com sucesso"
    )

    

    print("\nVoto registrado com sucesso!")
    print(f"Protocolo: {protocolo}")