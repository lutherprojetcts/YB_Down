import streamlit as st
import yt_dlp
import subprocess
import os
from pathlib import Path

st.set_page_config(page_title="MediaFusion Pro", layout="wide", page_icon="🚀")

# CSS Premium
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); color: white; }
.stButton>button { border-radius: 12px; height: 50px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

menu = st.sidebar.radio("📂 Menu", ["🔗 Gerar Links", "🎬 Unir / Otimizar Vídeo"])

# =======================
# 🔗 GERADOR DE LINKS
# =======================
if menu == "🔗 Gerar Links":
    st.title("🔗 Gerador de Links Diretos")
    url = st.text_input("Cole a URL do vídeo:")

    if st.button("🚀 Gerar Links de Alta Qualidade"):
        if url:
            with st.spinner("Extraindo a melhor qualidade disponível..."):
                try:
                    ydl_opts = {
                        'quiet': True,
                        'no_warnings': True,
                        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
                    }
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=False)
                        
                        # Seletores inteligentes que buscam o máximo disponível
                        video_stream = ydl.build_format_selector('bestvideo')(info)[0]
                        audio_stream = ydl.build_format_selector('bestaudio')(info)[0]

                        st.success(f"Qualidade detectada: {video_stream.get('resolution', 'N/A')}")
                        st.subheader("🎥 Vídeo (Direct Stream)")
                        st.code(video_stream['url'])
                        st.subheader("🎵 Áudio (Direct Stream)")
                        st.code(audio_stream['url'])
                        st.info("⚠️ Use estes links no menu 'Unir / Otimizar' ou baixe-os separadamente.")
                        
                except Exception as e:
                    st.error(f"Erro ao extrair links: {e}")

# =======================
# 🎬 MERGE PROFISSIONAL
# =======================
if menu == "🎬 Unir / Otimizar Vídeo":
    st.title("🎬 MediaFusion Engine")
    video_file = st.file_uploader("📹 Upload do vídeo (sem áudio)", type=["mp4","webm","mkv"])
    audio_file = st.file_uploader("🎵 Upload do áudio", type=["m4a","mp3","webm"])

    if video_file and audio_file:
        # Salvando arquivos com extensões genéricas
        with open("video_input", "wb") as f: f.write(video_file.getbuffer())
        with open("audio_input", "wb") as f: f.write(audio_file.getbuffer())

        if st.button("🚀 Processar e Unir"):
            output_file = "video_final.mp4"
            # O comando -c copy evita re-codificação, mantendo a qualidade original 4K/1080p
            comando = ["ffmpeg", "-y", "-i", "video_input", "-i", "audio_input", 
                       "-c", "copy", "-map", "0:v:0", "-map", "1:a:0", output_file]
            
            with st.spinner("Realizando o Merge (MUX) de alta velocidade..."):
                subprocess.run(comando)
            
            if os.path.exists(output_file):
                with open(output_file, "rb") as f:
                    st.download_button("📥 Baixar Vídeo Final", f, file_name="video_final.mp4")
            
            # Limpeza
            for f in ["video_input", "audio_input", "video_final.mp4"]:
                if os.path.exists(f): os.remove(f)
