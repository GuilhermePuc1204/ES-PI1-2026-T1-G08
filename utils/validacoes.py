import re
import mysql.connector
from mysql.connector import Error

# Função para validar formato e dígitos do CPF
def validar_cpf(cpf):
    """
    Valida um CPF conforme Anexo B do projeto.

    Args:
        cpf (str): CPF informado pelo usuário.

    Returns:
        bool: True se válido, False caso contrário.
    """
    cpf = re.sub(r'\D', '', cpf)

    # Tamanho e números repetidos
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    def calcular_digito(cpf_parcial, peso_inicial):
        soma = sum(int(cpf_parcial[i]) * (peso_inicial - i) for i in range(len(cpf_parcial)))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    dv1 = calcular_digito(cpf[:9], 10)
    dv2 = calcular_digito(cpf[:9] + str(dv1), 11)

    return cpf[-2:] == f"{dv1}{dv2}"

# Função para validar formato e dígitos do Título de Eleitor
def validar_titulo_eleitor(titulo):
    """
    Valida o Título de Eleitor conforme Anexo A do projeto.
    """

    import re

    titulo = re.sub(r'\D', '', titulo)

    if len(titulo) != 12:
        return False

    sequencial = titulo[:8]
    uf = titulo[8:10]
    dv_informados = titulo[10:]

    # ---------- Primeiro DV ----------
    pesos1 = [2, 3, 4, 5, 6, 7, 8, 9]
    soma1 = sum(int(sequencial[i]) * pesos1[i] for i in range(8))
    resto1 = soma1 % 11

    if resto1 == 10:
        dv1 = 0
    elif resto1 == 0 and uf in ("01", "02"):  # SP ou MG
        dv1 = 1
    else:
        dv1 = resto1

    # ---------- Segundo DV ----------
    pesos2 = [7, 8, 9]
    soma2 = (
        int(uf[0]) * pesos2[0] +
        int(uf[1]) * pesos2[1] +
        dv1 * pesos2[2]
    )
    resto2 = soma2 % 11

    if resto2 == 10:
        dv2 = 0
    elif resto2 == 0 and uf in ("01", "02"):  # SP ou MG
        dv2 = 1
    else:
        dv2 = resto2

    return dv_informados == f"{dv1}{dv2}"

def validar_documentos(cpf, titulo):
    """
    Validação completa de CPF e Título:
    - formato
    - cálculo matemático
    - unicidade no banco

    Returns:
        tuple(bool, str): status e mensagem
    """
    conexao = conectar_mysql()
    if not conexao:
        return False, "Erro de conexão com o banco"

    cpf_limpo = re.sub(r'\D', '', cpf)
    titulo_limpo = re.sub(r'\D', '', titulo)

    if not validar_cpf(cpf_limpo):
        return False, "CPF inválido"

    if not validar_titulo_eleitor(titulo_limpo):
        return False, "Título de eleitor inválido"

    if cpf_existe(cpf_limpo, conexao):
        return False, "CPF já cadastrado"

    if titulo_existe(titulo_limpo, conexao):
        return False, "Título já cadastrado"

    return True, "Documentos válidos"