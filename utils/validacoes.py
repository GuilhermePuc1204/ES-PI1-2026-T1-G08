import re

# Função para validar formato e dígitos verificadores do CPF
def validar_cpf(cpf):
    # Remove pontos, traços e qualquer caractere não numérico
    cpf = re.sub(r'\D', '', cpf)

    # Verifica se tem exatamente 11 dígitos e não é uma sequência repetida (ex: 111.111.111-11)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    # Calcula um dígito verificador do CPF usando pesos decrescentes a partir de peso_inicial
    def calcular_digito(cpf_parcial, peso_inicial):
        soma = sum(int(cpf_parcial[i]) * (peso_inicial - i) for i in range(len(cpf_parcial)))
        resto = soma % 11
        # Se o resto for menor que 2, o dígito é 0; caso contrário, é 11 - resto
        return 0 if resto < 2 else 11 - resto

    # Calcula o primeiro dígito verificador usando os 9 primeiros dígitos com pesos de 10 a 2
    dv1 = calcular_digito(cpf[:9], 10)

    # Calcula o segundo dígito verificador usando os 9 primeiros dígitos + dv1, com pesos de 11 a 2
    dv2 = calcular_digito(cpf[:9] + str(dv1), 11)

    # Compara os dois últimos dígitos do CPF com os dígitos verificadores calculados
    return cpf[-2:] == f"{dv1}{dv2}"


# Função para validar formato e dígitos verificadores do Título de Eleitor
def validar_titulo_eleitor(titulo):
    # Remove qualquer caractere não numérico
    titulo = re.sub(r'\D', '', titulo)

    # Título de eleitor deve ter exatamente 12 dígitos
    if len(titulo) != 12:
        return False

    # Divide o título nas suas três partes:
    # - sequencial: 8 dígitos identificadores
    # - uf: 2 dígitos do código do estado (ex: 01 = SP, 02 = MG)
    # - dv_informados: 2 dígitos verificadores fornecidos
    sequencial = titulo[:8]
    uf = titulo[8:10]
    dv_informados = titulo[10:]

    # --- Cálculo do primeiro dígito verificador ---
    # Multiplica cada dígito do sequencial pelos pesos 2 a 9 e soma os resultados
    pesos1 = [2, 3, 4, 5, 6, 7, 8, 9]
    soma1 = sum(int(sequencial[i]) * pesos1[i] for i in range(8))
    resto1 = soma1 % 11

    if resto1 == 10:
        # Resto 10 não é dígito válido, substitui por 0
        dv1 = 0
    elif resto1 == 0 and uf in ("01", "02"):
        # Exceção para SP (01) e MG (02): resto 0 vira 1
        dv1 = 1
    else:
        dv1 = resto1

    # --- Cálculo do segundo dígito verificador ---
    # Usa os dois dígitos da UF e o primeiro DV calculado, com pesos 7, 8 e 9
    pesos2 = [7, 8, 9]
    soma2 = (
        int(uf[0]) * pesos2[0] +
        int(uf[1]) * pesos2[1] +
        dv1 * pesos2[2]
    )
    resto2 = soma2 % 11

    if resto2 == 10:
        # Resto 10 não é dígito válido, substitui por 0
        dv2 = 0
    elif resto2 == 0 and uf in ("01", "02"):
        # Exceção para SP (01) e MG (02): resto 0 vira 1
        dv2 = 1
    else:
        dv2 = resto2

    # Compara os dígitos verificadores calculados com os informados no título
    return dv_informados == f"{dv1}{dv2}"
