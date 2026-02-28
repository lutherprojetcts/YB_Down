import streamlit as st
import subprocess
import os
import shutil
from pathlib import Path

st.set_page_config(
    page_title="Video Merger Pro",
    layout="centered",
    page_icon="🎬"
)

# ====== CSS MODERNO MOBILE FRIENDLY ======
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

h1, h2, h3 {
    text-align: center;
}

.block-container {
    padding-top: 2rem;
}

.stButton>button {
    width: 100%;
    border-radius: 12px;
    height: 50px;
    font-size: 18px;
    font-weight: bold;
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    color: white;
    border: none;
}

.stDownloadButton>button {
    width: 100%;
    border-radius: 12px;
    height: 50px;
    font-size: 18px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("🎬 Video Merger Pro")
st.caption("Upload do vídeo + áudio separados e gere o MP4 final em alta qualidade.")

# ====== UPLOAD ======
video_file = st.file_uploader(
    "📹 Upload do vídeo (sem áudio)",
    type=["mp4", "webm", "mkv"]
)

audio_file = st.file_uploader(
    "🎵 Upload do áudio",
    type=["m4a", "mp3", "webm"]
)

output_path = Path("final_output.mp4")

def limpar_arquivos():
    for file in ["video_input", "audio_input", "final_output.mp4"]:
        if os.path.exists(file):
            os.remove(file)

if video_file and audio_file:

    st.success("Arquivos carregados com sucesso!")

    if st.button("🚀 Gerar Vídeo Final"):

        with st.spinner("Processando... Isso pode levar alguns minutos para vídeos grandes."):

            limpar_arquivos()

            # ====== SALVANDO EM STREAM (BAIXO USO RAM) ======
            with open("video_input", "wb") as f:
                shutil.copyfileobj(video_file, f)

            with open("audio_input", "wb") as f:
                shutil.copyfileobj(audio_file, f)

            # ====== MERGE OTIMIZADO (SEM REENCODE) ======
            comando = [
                "ffmpeg",
                "-i", "video_input",
                "-i", "audio_input",
                "-c", "copy",
                "-map", "0:v:0",
                "-map", "1:a:0",
                "-movflags", "+faststart",
                "final_output.mp4"
            ]

            subprocess.run(
                comando,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

        if output_path.exists():

            st.success("✅ Vídeo gerado com sucesso!")

            with open(output_path, "rb") as f:
                st.download_button(
                    "📥 Baixar Vídeo Final",
                    f,
                    file_name="video_final.mp4",
                    mime="video/mp4"
                )

            # limpeza automática após renderizar botão
            limpar_arquivos()
