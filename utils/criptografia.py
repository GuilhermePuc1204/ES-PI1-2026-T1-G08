alfabeto=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
chave_hill=[[3, 3], [2, 5]]

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