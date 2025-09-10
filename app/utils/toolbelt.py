


import unicodedata


def normalize_text(text: str, lowercase: bool = True, replace_spaces: bool = True) -> str:
    """
     This function normalizes the text by removing accents and replacing spaces with underscores.
    """
    # 1. Normalize the text to NFD to separate accents
    text_nfd = unicodedata.normalize('NFD', text)
    # 2. Filter only the characters that are not accent marks (Mn)
    text_without_accents = ''.join(
        char for char in text_nfd
        if unicodedata.category(char) != 'Mn'
    )

    if replace_spaces:
        normalized_text = text_without_accents.replace(' ', '_')
    else:
        normalized_text = text_without_accents
        
    if lowercase:
        normalized_text = normalized_text.lower()
    normalized_text = normalized_text.replace('/', '_')
    return normalized_text


def validate_rut(rut: str) -> bool:
    # Limpiar el RUT: eliminar puntos y guion, y convertir a mayúsculas
    rut = rut.replace('.', '').replace('-', '').upper()
    
    # El RUT debe tener al menos 2 caracteres (número + dígito verificador)
    if len(rut) < 2:
        return False

    # Separar número y dígito verificador
    num = rut[:-1]
    dv = rut[-1]

    # Validar que el número solo tenga dígitos
    if not num.isdigit():
        return False
    
    # Algoritmo módulo 11 para calcular dígito verificador
    suma = 0
    multiplicador = 2

    for digit in reversed(num):
        suma += int(digit) * multiplicador
        multiplicador += 1
        if multiplicador > 7:
            multiplicador = 2
    
    resto = suma % 11
    dv_calculado = ''
    diff = 11 - resto
    if diff == 11:
        dv_calculado = '0'
    elif diff == 10:
        dv_calculado = 'K'
    else:
        dv_calculado = str(diff)
    
    # Comparar dígito verificador calculado con el ingresado
    return dv_calculado == dv