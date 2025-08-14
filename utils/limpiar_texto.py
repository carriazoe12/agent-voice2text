import re

def limpiar_transcripcion(texto: str) -> str:
    """
    Limpia y estandariza un bloque de texto segun reglas especificas.

    Pasos de limpieza:
    1. Convierte todo el texto a mayúsculas.
    2. Elimina los signos de puntuación (puntos, comas, etc.).
    3. Elimina cualquier otro caracter que no sea letra, numero o espacio.
    4. Normaliza los espacios en blanco múltiples a uno solo.

    Args:
        texto (str): El texto a limpiar.

    Returns:
        str: El texto limpio y estandarizado.
    """

    if not isinstance(texto, str):
        return ""

    # Convertir a mayusculas
    texto_mayusculas = texto.upper()
    
    # Eliminar signos de puntuación y caracteres especiales
    # A-Z, Ñ, ÁÉÍÓÚ, Ü y dígitos
    texto_permitido = re.sub(r'[^0-9A-ZÁÉÍÓÚÜÑ\s]', ' ', texto_mayusculas)

    # Normalizar espacios múltiples a uno solo
    texto_limpio = re.sub(r'\s+', ' ', texto_permitido).strip()
    
    return texto_limpio