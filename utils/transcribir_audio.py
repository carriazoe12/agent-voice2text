import whisper


_WHISPER_MODEL = None

def _cargar_modelo() -> whisper.Whisper:
    global _WHISPER_MODEL
    if _WHISPER_MODEL is None:
        _WHISPER_MODEL = whisper.load_model("base") # 'small', 'medium' o 'large'.
    return _WHISPER_MODEL

def transcribir_audio(audio_path: str) -> str:
    """
    Transcribe un archivo de audio utilizando el modelo Whisper de OpenAI.

    Esta función carga el modelo 'base' de Whisper, que es un buen equilibrio
    entre velocidad y precisión, y es multilingüe.

    Args:
        audio_path (str): La ruta al archivo de audio a transcribir (ej. .wav, .mp3).

    Returns:
        str: El texto transcrito de la conversación completa.
        
    Raises:
        Exception: Si ocurre un error durante la carga del modelo o la transcripción.
    """
    try:
        
        model = _cargar_modelo()
        
        # Realizar la transcripción
        result = model.transcribe(audio_path, fp16=False)
        
        # Obtener el texto transcrito
        transcripcion = result["text"]
        
        return transcripcion

    except Exception as e:

        raise Exception(f"Error durante la transcripción de audio: {e}")