import streamlit as st
import os
from utils.transcribir_audio import transcribir_audio
from utils.preprocesar_audio import preprocesar_audio
from utils.limpiar_texto import limpiar_transcripcion
from utils.analisis_llm import extraer_dialogo_agente_con_llm
import time
from utils.transcribir_audio_diarizado import transcribir_audio_diarizado

st.set_page_config(
    page_title="Procesador de Llamadas con IA",
    page_icon="🤖",
    layout="wide"
)

# --- Directorios ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENTRADA_DIR = os.path.join(BASE_DIR, "audio_in")
SALIDA_DIR = os.path.join(BASE_DIR, "audio_out")
TRANSCRIPCIONES_DIR = os.path.join(BASE_DIR, "transcripciones")

os.makedirs(ENTRADA_DIR, exist_ok=True)
os.makedirs(SALIDA_DIR, exist_ok=True)
os.makedirs(TRANSCRIPCIONES_DIR, exist_ok=True)


# --- Sidebar ---
with st.sidebar:
    st.title("📄 Instrucciones")
    st.info(
        """
        **Este sistema utiliza IA para procesar llamadas y extraer el diálogo del agente.**

        1.  **Ingrese su API Key** de OpenAI.
        2.  **Cargue un archivo de audio** (`.wav`, `.mp3`).
        3.  **Haga clic en "Procesar con IA"**.
        4.  El sistema:
            - Limpiará el audio.
            - Transcribirá la conversación completa.
            - **Usará un LLM para identificar y separar el diálogo del agente.**
            - Estandarizará el texto resultante.
        5.  **Revise los resultados**.
        """
    )
    
    api_key = st.text_input("🔑 OpenAI API Key", type="password", help="Tu clave de API de OpenAI es necesaria para el análisis del diálogo.")


# --- Logica ---
st.title("🤖 Procesamiento de Llamadas Asistido por LLM")
st.markdown("---")

uploaded_file = st.file_uploader(
    "Cargue el archivo de audio de la llamada",
    type=["wav", "mp3", "m4a"]
)

if uploaded_file is not None:
    input_path = os.path.join(ENTRADA_DIR, uploaded_file.name)
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.markdown("### Archivo Cargado")
    st.audio(input_path, format='audio/wav')

    
    if st.button("▶️ Procesar con IA", use_container_width=True, type="primary", disabled=(not api_key)):
        
        with st.spinner("Procesando... Este proceso puede tardar unos minutos."):
            try:
                # Preprocesamiento (mono, normalizacion, reduccion de ruido, eliminacion de silencios)
                st.write("1️⃣ **Limpiando y preparando el audio...**")
                audio_preprocesado_path = preprocesar_audio(input_path, SALIDA_DIR)

                # PASO 1: Transcripcion 
                st.write("2️⃣ **Transcribiendo la conversación completa (Agente y Cliente)...**")
                transcripcion_completa = transcribir_audio(audio_preprocesado_path)
                # Alternativa con diarización local (Whisper + pyannote):  
                #transcripcion_completa = transcribir_audio_diarizado(audio_preprocesado_path)   

                # PASO 2: Analisis con LLM para extraer dialogo del agente
                st.write("3️⃣ **Usando IA para identificar el diálogo del agente...**")
                dialogo_agente = extraer_dialogo_agente_con_llm(transcripcion_completa, api_key)

                # PASO 3: Limpieza del texto
                st.write("4️⃣ **Estandarizando el texto del agente...**")
                transcripcion_limpia_agente = limpiar_transcripcion(dialogo_agente)
                
                # PASO 4: Guardar la transcripci0n
                st.write("5️⃣ **Guardando resultado final...**")
                base_filename = os.path.splitext(uploaded_file.name)[0]
                output_txt_path = os.path.join(TRANSCRIPCIONES_DIR, f"{base_filename}_agente.txt")

                with open(output_txt_path, "w", encoding="utf-8") as f:
                    f.write(transcripcion_limpia_agente)
                
                st.success("¡Proceso completado con éxito!")
                
                st.session_state.results = {
                    "original_audio": input_path,
                    "full_transcription": transcripcion_completa,
                    "final_agent_text": transcripcion_limpia_agente
                }
                
                time.sleep(1)
                st.rerun()

            except Exception as e:
                st.error(f"Ocurrió un error: {e}")

if 'results' in st.session_state:
    st.markdown("---")
    st.markdown("## ✅ Resultados del Procesamiento")

    st.markdown("### Transcripción Completa")
    st.text_area("Transcripción Original", st.session_state.results["full_transcription"], height=150)
    
    st.markdown("### Transcripción Final del Agente (Extraída por IA)")
    st.text_area("Texto Limpio y Estandarizado", st.session_state.results["final_agent_text"], height=200)