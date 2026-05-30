def validar_cpf(cpf):
    """
    Valida o CPF utilizando o algoritmo oficial de dígitos verificadores.

    Remove caracteres não numéricos da entrada, rejeita CPFs com todos os
    dígitos iguais (ex: 111.111.111-11) e recalcula os dois dígitos
    verificadores (10º e 11º) a partir dos nove primeiros dígitos,
    comparando-os com os informados.

    Args:
        cpf (str): CPF informado pelo usuário, com ou sem formatação
            (pontos e traço).

    Returns:
        bool: True se o CPF for matematicamente válido, False caso
        contrário.
    """
    cpf_limpo = ""
    
    for c in cpf:
        if c.isdigit():
            cpf_limpo += c

    if len(cpf_limpo) != 11 or cpf_limpo == cpf_limpo[0] * 11:
        return False

    def calcular_digito(cpf_parcial, peso_inicial):
        """
        Calcula um dígito verificador do CPF.

        Multiplica cada algarismo do CPF parcial por pesos decrescentes
        a partir de peso_inicial, soma os resultados e aplica a regra do
        resto da divisão por 11: se o resto for menor que 2 o dígito é
        0; caso contrário, o dígito é 11 - resto.

        Args:
            cpf_parcial (str): Sequência inicial do CPF a ser usada no
                cálculo (9 dígitos para o primeiro DV, 10 para o segundo).
            peso_inicial (int): Valor inicial dos pesos decrescentes
                (10 para o primeiro DV, 11 para o segundo).

        Returns:
            int: Dígito verificador calculado (0 a 9).
        """
        soma = sum(int(cpf_parcial[i]) * (peso_inicial - i) for i in range(len(cpf_parcial)))
        resto = soma % 11
        # Se o resto for menor que 2, o dígito é 0; caso contrário, é 11 - resto
        return 0 if resto < 2 else 11 - resto

    dv1 = calcular_digito(cpf_limpo[:9], 10)

    dv2 = calcular_digito(cpf_limpo[:9] + str(dv1), 11)

    return cpf_limpo[-2:] == f"{dv1}{dv2}"


def validar_titulo_eleitor(titulo):
    """
    Valida o Título de Eleitor utilizando o algoritmo de dígitos verificadores.

    O título possui 12 dígitos: 8 sequenciais, 2 da Unidade Federativa (UF)
    e 2 verificadores. O primeiro DV é calculado sobre os 8 sequenciais
    com pesos de 2 a 9; o segundo DV é calculado sobre a UF e o primeiro DV
    com pesos 7, 8 e 9. Em ambos os cálculos, resto 10 vira 0, e nos
    estados SP (01) e MG (02), resto 0 vira 1.

    Args:
        titulo (str): Número do título de eleitor com ou sem formatação.

    Returns:
        bool: True se o título for matematicamente válido, False caso
        contrário.
    """
    titulo_limpo = ""
    for c in titulo:
        if c.isdigit():
            titulo_limpo += c


    if len(titulo_limpo) != 12:
        return False

   
    sequencial = titulo_limpo[:8]
    uf = titulo_limpo[8:10]
    dv_informados = titulo_limpo[10:]

    pesos1 = [2, 3, 4, 5, 6, 7, 8, 9]
    soma1 = sum(int(sequencial[i]) * pesos1[i] for i in range(8))
    resto1 = soma1 % 11

    if resto1 == 10:
        dv1 = 0
    elif resto1 == 0 and uf in ("01", "02"):
        dv1 = 1
    else:
        dv1 = resto1

    pesos2 = [7, 8, 9]
    soma2 = (
        int(uf[0]) * pesos2[0] +
        int(uf[1]) * pesos2[1] +
        dv1 * pesos2[2]
    )
    resto2 = soma2 % 11

    if resto2 == 10:
        dv2 = 0
    elif resto2 == 0 and uf in ("01", "02"):
        dv2 = 1
    else:
        dv2 = resto2

    return dv_informados == f"{dv1}{dv2}"
