"""
Módulo: validacoes.py

Responsabilidade:
Este módulo concentra todas as validações matemáticas dos documentos
utilizados no sistema, conforme especificado nos Anexos A e B do projeto.

Documentos validados:
- CPF (Cadastro de Pessoa Física)
- Título de Eleitor

Observações importantes:
- Este módulo NÃO acessa banco de dados
- Este módulo NÃO realiza criptografia
- Este módulo NÃO verifica unicidade
- Seu único papel é validar a consistência matemática dos documentos
"""

import re  # Utilizado para normalização dos documentos (remoção de caracteres não numéricos)


# ==========================================================
# VALIDAÇÃO DO CPF (ANEXO B)
# ==========================================================
def validar_cpf(cpf):
    """
    Valida um CPF conforme as regras descritas no Anexo B do projeto.

    Etapas da validação:
    1. Remoção de caracteres não numéricos
    2. Verificação de tamanho (11 dígitos)
    3. Rejeição de CPFs com todos os dígitos iguais
    4. Cálculo e verificação dos dois dígitos verificadores

    Args:
        cpf (str): CPF informado pelo usuário.

    Returns:
        bool: True se o CPF for válido, False caso contrário.
    """

    # Remove qualquer caractere que não seja número
    cpf = re.sub(r'\D', '', cpf)

    # Verifica tamanho e rejeita CPFs com todos os dígitos iguais
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    # ------------------------------------------------------
    # Função interna para cálculo do dígito verificador
    # ------------------------------------------------------
    def calcular_digito(cpf_parcial, peso_inicial):
        """
        Calcula um dígito verificador do CPF.

        Args:
            cpf_parcial (str): Parte do CPF utilizada no cálculo.
            peso_inicial (int): Peso inicial da sequência.

        Returns:
            int: Dígito verificador calculado.
        """
        soma = sum(
            int(cpf_parcial[i]) * (peso_inicial - i)
            for i in range(len(cpf_parcial))
        )
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    # Cálculo dos dois dígitos verificadores
    dv1 = calcular_digito(cpf[:9], 10)
    dv2 = calcular_digito(cpf[:9] + str(dv1), 11)

    # Verifica se os dígitos calculados coincidem com os informados
    return cpf[-2:] == f"{dv1}{dv2}"


# ==========================================================
# VALIDAÇÃO DO TÍTULO DE ELEITOR (ANEXO A)
# ==========================================================
def validar_titulo_eleitor(titulo):
    """
    Valida o Título de Eleitor conforme as regras descritas no Anexo A do projeto.

    Estrutura do título:
    - 8 dígitos: número sequencial
    - 2 dígitos: UF
    - 2 dígitos: dígitos verificadores (DV1 e DV2)

    Regras especiais:
    - Para títulos emitidos em SP (01) e MG (02), quando o resto for 0,
      o dígito verificador assume o valor 1.

    Args:
        titulo (str): Título de eleitor informado pelo usuário.

    Returns:
        bool: True se o título for válido, False caso contrário.
    """

    # Remove qualquer caractere que não seja número
    titulo = re.sub(r'\D', '', titulo)

    # Verifica se o título possui exatamente 12 dígitos
    if len(titulo) != 12:
        return False

    # Separação das partes do título
    sequencial = titulo[:8]
    uf = titulo[8:10]
    dv_informados = titulo[10:]

    # ------------------------------------------------------
    # Cálculo do primeiro dígito verificador (DV1)
    # ------------------------------------------------------
    pesos1 = [2, 3, 4, 5, 6, 7, 8, 9]
    soma1 = sum(int(sequencial[i]) * pesos1[i] for i in range(8))
    resto1 = soma1 % 11

    if resto1 == 10:
        dv1 = 0
    elif resto1 == 0 and uf in ("01", "02"):  # SP ou MG
        dv1 = 1
    else:
        dv1 = resto1

    # ------------------------------------------------------
    # Cálculo do segundo dígito verificador (DV2)
    # ------------------------------------------------------
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

    # Verifica se os dígitos calculados coincidem com os informados
    return dv_informados == f"{dv1}{dv2}"