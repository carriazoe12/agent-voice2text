import os
from pydub import AudioSegment, effects
from pydub.silence import split_on_silence

def preprocesar_audio(input_path: str, output_dir: str) -> str:
    """
    Preprocesa un archivo de audio para mejorar la transcripcion:
    - Convierte a mono 
    - Normaliza niveles
    - Atenúa ruidos comunes
    - Elimina silencios prolongados
    - Exporta en WAV listo para Whisper

    Args:
        input_path (str): Ruta al archivo de audio de entrada (.wav, .mp3, etc.)
        output_dir (str): Directorio donde se guardará el audio preprocesado

    Returns:
        str: Ruta al archivo WAV preprocesado
    """
    try:
        audio = AudioSegment.from_file(input_path)
    except Exception as e:
        raise IOError(f"No se pudo cargar el archivo de audio: {input_path}. Error: {e}")

    # Asegurar mono y normalizar
    if audio.channels != 1:
        audio = audio.set_channels(1)
    audio = effects.normalize(audio)

    # Filtros para atenuar ruidos comunes https://medium.com/analytics-vidhya/how-to-filter-noise-with-a-low-pass-filter-python-885223e5e9b7

    audio = audio.high_pass_filter(100) # reduce zumbidos de baja frecuencia reduce zumbidos de baja frecuencia
    audio = audio.low_pass_filter(8000) # reduce siseo/agudos muy altos

    # Eliminar silencios
    chunks = split_on_silence(
        audio,
        min_silence_len=600,               # >= 0.6s de silencio
        silence_thresh=audio.dBFS - 14,  # 14 dB por debajo del promedio
        keep_silence=250                   # evitar cortes bruscos 
    )

    if not chunks:
        audio_limpio = audio
    else:
        audio_limpio = sum(chunks)

    # Exportar audio
    base_filename = os.path.splitext(os.path.basename(input_path))[0]
    output_filename = f"{base_filename}_preprocesado.wav"
    output_path = os.path.join(output_dir, output_filename)
    audio_limpio.export(output_path, format="wav")

    return output_path