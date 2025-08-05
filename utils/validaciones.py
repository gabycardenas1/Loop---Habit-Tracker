def validarCedula(cedula: str) -> bool: 
    # Función que valida la cédula de acuerdo a la normativa actual.
    if len(cedula) != 10 or not cedula.isdigit():
        return False
    provincia = int(cedula[0:2])
    tercerDigito = int(cedula[2])
    if provincia < 1 or provincia > 24 or tercerDigito > 6:
        return False
    coeficiente = [2,1,2,1,2,1,2,1,2]
    suma = 0
    for i in range(9):
        p = int(cedula[i]) * coeficiente[i]
        if p >= 10:
            p -= 9
        suma += p
    digito = 10 - (suma % 10) if (suma % 10) != 0 else 0
    return digito == int(cedula[9])

def validar_tarjeta(numero):
    # Valida si el número de tarjeta es numérico, de 16 dígitos y pasa el algoritmo de Luhn.
    if not numero.isdigit() or len(numero) != 16:
        return False

    # Algoritmo de Luhn
    suma = 0
    alternar = False
    for digito in reversed(numero):
        n = int(digito)
        if alternar:
            n *= 2
            if n > 9:
                n -= 9
        suma += n
        alternar = not alternar

    return suma % 10 == 0

def validar_clave_seguridad(clave):
    # Valida si la clave de seguridad tiene 3 o 4 dígitos numéricos.
    return clave.isdigit() and len(clave) in [3, 4]

