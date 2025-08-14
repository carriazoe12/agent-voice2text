from typing import List, Tuple
import os
from dotenv import load_dotenv
import whisper
from pyannote.audio import Pipeline
from pyannote_whisper.utils import diarize_text


_WHISPER_DIAR_MODEL = None


def _cargar_modelo_whisper() -> whisper.Whisper:
    global _WHISPER_DIAR_MODEL
    if _WHISPER_DIAR_MODEL is None:
        _WHISPER_DIAR_MODEL = whisper.load_model("base")
    return _WHISPER_DIAR_MODEL


def transcribir_audio_diarizado(audio_path: str) -> str:
    """
    Transcribe el audio localmente con Whisper y realiza diarización con pyannote.audio,
    generando una transcripción con etiquetas de hablante (SPEAKER_XX) por segmento.

    Args:
        audio_path (str): Ruta al archivo de audio a transcribir.

    Returns:
        str: Texto final con formato `SPEAKER_XX: frase`.
    """
    # Cargar variable de entorno, token de Hugging Face
    load_dotenv()
    token = os.getenv("HUGGINGFACE_TOKEN")
    if not token:
        raise ValueError(
            "Se requiere un token de Hugging Face (HUGGINGFACE_TOKEN en .env) para la diarización."
        )

    model = _cargar_modelo_whisper()

    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization", use_auth_token=token
    )

    # Whisper + pyannote
    asr_result = model.transcribe(audio_path, fp16=False)

    diarization_result = pipeline(audio_path) #num_speakers=2 

    final_result: List[Tuple] = diarize_text(asr_result, diarization_result)

    lines: List[str] = []
    for segment, speaker, sentence in final_result: # .start y .end en segment

        lines.append(f"{speaker}: {sentence}")

    return "\n".join(lines)


