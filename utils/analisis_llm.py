from openai import OpenAI


def extraer_dialogo_agente_con_llm(transcripcion_completa: str, api_key: str) -> str:
    """
    Utiliza un LLM (modelo de OpenAI) para analizar una transcripción y extraer
    únicamente las líneas de diálogo del agente.

    Args:
        transcripcion_completa (str): El texto completo de la transcripción de la llamada.
        api_key (str): La clave de API para el servicio de OpenAI.

    Returns:
        str: Un string que contiene únicamente el diálogo del agente.
        
    Raises:
        ValueError: Si la clave de API no es proporcionada.
        Exception: Para errores durante la llamada a la API de OpenAI.
    """
    if not api_key:
        raise ValueError("La clave de API de OpenAI es requerida para esta función.")

    client = OpenAI(api_key=api_key)

    # Creamos un prompt para el LLM, un rol, un contexto claro, la tarea específica y el formato de salida
    prompt = """
    Eres un asistente experto en el analisis de transcripciones de centros de llamadas.
    Tu tarea es leer la siguiente transcripción de una conversación entre un 'Agente' y un 'Cliente'.
    Debes identificar y extraer UNICAMENTE las líneas de diálogo que pertenecen al 'Agente'.

    El Agente normalmente es quien saluda, se identifica en nombre de la empresa, realiza preguntas de verificación, y ofrece soluciones o guía al cliente. El Cliente es quien describe un problema o solicita ayuda.

    Devuelve solo el texto del agente, concatenado en un solo bloque de texto. No incluyas prefijos como "Agente:" o "SPEAKER_00:", ni ningún otro texto explicativo. Solo el diálogo.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": transcripcion_completa}
            ],
            temperature=0.0,
            max_tokens=1500
        )
        dialogo_agente = response.choices[0].message.content.strip()
        return dialogo_agente
    except Exception as e:
        raise Exception(f"Error al contactar la API de OpenAI: {e}")