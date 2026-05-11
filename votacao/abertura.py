from datetime import datetime
from database.conexao import conexao, cursor
from utils.criptografia import criptografar_cpf, criptografar_chave_acesso


def abrir_votacao():
    print("\n=== ABERTURA DO SISTEMA DE VOTAÇÃO ===")

    # Lê o título de eleitor do mesário para identificação
    titulo = input("Título de eleitor do mesário: ").strip()

    # Busca o eleitor no banco pelo título informado
    cursor.execute(
        "SELECT id, nome, cpf, mesario, chave_acesso FROM eleitores WHERE titulo_eleitor = %s",
        (titulo,)
    )
    eleitor = cursor.fetchone()

    # Se não encontrou nenhum registro, encerra
    if not eleitor:
        print("Mesário não encontrado.")
        return

    id_eleitor, nome, cpf_criptografado, mesario, chave_armazenada = eleitor

    # Verifica se o eleitor encontrado realmente é mesário
    if not mesario:
        print("Eleitor não é mesário.")
        return

    # Lê os 4 primeiros dígitos do CPF para autenticação
    primeiros_digitos = input("4 primeiros dígitos do CPF: ").strip()
    if len(primeiros_digitos) != 4 or not primeiros_digitos.isdigit():
        print("Entrada inválida.")
        return

    # Criptografa os 4 dígitos e compara com o início do CPF armazenado
    # (Hill opera em pares, então os 4 primeiros dígitos geram os 4 primeiros chars do CPF criptografado)
    if criptografar_cpf(primeiros_digitos) != cpf_criptografado[:4]:
        print("Autenticação falhou.")
        _registrar_log(f"Tentativa de acesso negada para título {titulo}")
        return

    # Lê a chave de acesso do mesário
    chave = input("Chave de acesso: ").strip()

    # Criptografa a chave informada e compara com a armazenada no banco
    if criptografar_chave_acesso(chave) != chave_armazenada:
        print("Chave de acesso incorreta.")
        _registrar_log(f"Tentativa de acesso negada para título {titulo}")
        return

    print(f"\nMesário autenticado: {nome}")

    # Verifica se já existe uma votação aberta para evitar dupla abertura
    cursor.execute("SELECT status FROM urna ORDER BY id DESC LIMIT 1")
    urna = cursor.fetchone()
    if urna and urna[0] == "aberta":
        print("Sistema já está aberto.")
        return

    # --- ZERÉSIMA ---
    print("\n=== ZERÉSIMA ===")

    # Remove todos os votos registrados anteriormente
    cursor.execute("DELETE FROM votos")

    # Reseta o status de todos os eleitores para "Não votou"
    cursor.execute("UPDATE eleitores SET status_voto = 'Não votou'")
    conexao.commit()

    # Busca os candidatos em ordem alfabética para exibir com votos zerados
    cursor.execute("SELECT nome, numero, partido FROM candidatos ORDER BY nome")
    candidatos = cursor.fetchall()

    # Exige ao menos um candidato cadastrado para abrir a votação
    if not candidatos:
        print("Nenhum candidato cadastrado. Cadastre candidatos antes de abrir a votação.")
        return

    print("Candidatos com votos zerados:")
    for c in candidatos:
        print(f"  {c[0]} - Nº {c[1]} ({c[2]}): 0 votos")

    # Registra a abertura na tabela urna com data e hora atuais
    agora = datetime.now()
    cursor.execute(
        "INSERT INTO urna (status, data_abertura) VALUES (%s, %s)",
        ("aberta", agora)
    )

    # Registra o evento de abertura no log de auditoria
    _registrar_log(f"Votação aberta pelo mesário {nome}")
    conexao.commit()

    print(f"\nSistema aberto em {agora.strftime('%d/%m/%Y %H:%M:%S')}.")


def _registrar_log(evento):
    # Insere um registro de evento na tabela de logs com data e hora atuais
    cursor.execute(
        "INSERT INTO logs (data_hora, evento) VALUES (%s, %s)",
        (datetime.now(), evento)
    )
