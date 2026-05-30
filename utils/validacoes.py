def validar_cpf(cpf):
    cpf_limpo = ""
    
    for c in cpf:
        if c.isdigit():
            cpf_limpo += c

    if len(cpf_limpo) != 11 or cpf_limpo == cpf_limpo[0] * 11:
        return False

    def calcular_digito(cpf_parcial, peso_inicial):
        soma = sum(int(cpf_parcial[i]) * (peso_inicial - i) for i in range(len(cpf_parcial)))
        resto = soma % 11
        # Se o resto for menor que 2, o dígito é 0; caso contrário, é 11 - resto
        return 0 if resto < 2 else 11 - resto

    dv1 = calcular_digito(cpf_limpo[:9], 10)

    dv2 = calcular_digito(cpf_limpo[:9] + str(dv1), 11)

    return cpf_limpo[-2:] == f"{dv1}{dv2}"


def validar_titulo_eleitor(titulo):  
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
