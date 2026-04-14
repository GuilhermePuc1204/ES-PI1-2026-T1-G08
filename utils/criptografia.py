alfabeto=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
chave_hill=[[3, 3], [2, 5]]

alfabeto_chave = [
    "A","B","C","D","E","F","G","H","I","J","K","L","M",
    "N","O","P","Q","R","S","T","U","V","W","X","Y","Z",
    "0","1","2","3","4","5","6","7","8","9"
]

def criptografar_cpf(cpf):
    """
    Criptografa um cpf utilizando a cifra de Hill.

    Args:
        cpf (str): CPF válido contendo apenas números.

    Returns:
        Str: CPF criptografado.
    """
    # Converte cada digito do cpf para inteiro
    cpf = [int(d) for d in cpf]

    #Garante quantidade par de elementos.
    if len(cpf) % 2 !=0:
        cpf.append(0)

    resultado = []

    #Processa em blocos de 2
    for i in range(0, len(cpf), 2):
        x =cpf[i]
        y =cpf[i+1]

        # Cifra de Hill / Multiplicação de matrizes
        r1 = (chave_hill[0][0] * x + chave_hill[0][1] * y) % len(alfabeto)
        r2 = (chave_hill[1][0] * x + chave_hill[1][1] * y) % len(alfabeto)

        # Conversão para letras
        resultado.append(alfabeto[r1])
        resultado.append(alfabeto[r2])
        
    # Retorno do texto criptografado
    return "".join(resultado)

def criptografar_chave_acesso(chave):
    """
    Criptografa a chave de accesso utilizando a cifra de Hill.
    Args:
        chave (str): Chave de acesso em texto claro.

    Returns:
        str: Chave de acesso criptografada.
    """
    
# Converte caracteres para índices do alfabeto
    valores = []
    for c in chave.upper():
        if c not in alfabeto_chave:
            raise ValueError("Caractere inválido na chave de acesso")
        valores.append(alfabeto_chave.index(c))

    # Garante quantidade par
    if len(valores) % 2 != 0:
        valores.append(0)

    resultado = []

    for i in range(0, len(valores), 2):
        x = valores[i]
        y = valores[i + 1]

        r1 = (chave_hill[0][0] * x + chave_hill[0][1] * y) % len(alfabeto_chave)
        r2 = (chave_hill[1][0] * x + chave_hill[1][1] * y) % len(alfabeto_chave)

        resultado.append(alfabeto_chave[r1])
        resultado.append(alfabeto_chave[r2])

    return "".join(resultado)
