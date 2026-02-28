import streamlit as st
import yt_dlp
import subprocess
import os
import shutil
import json
from pathlib import Path

st.set_page_config(page_title="MediaFusion Pro", layout="wide", page_icon="🚀")

# CSS mantido igual
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

    if st.button("🚀 Gerar Links"):
        if url:
            with st.spinner("Extraindo streams..."):
                try:
                    # Configuração para evitar erro 403 e obter links diretos
                    ydl_opts = {
                        'quiet': True,
                        'no_warnings': True,
                        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
                    }
                    
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=False)
                        
                        # Buscamos formatos mp4 específicos para garantir URL direta
                        # 137 é geralmente 1080p, 140 é áudio m4a
                        video_stream = next((f for f in info['formats'] if f['format_id'] == '137' or (f.get('height') == 1080 and f['ext'] == 'mp4')), info['formats'][-1])
                        audio_stream = next((f for f in info['formats'] if f['format_id'] == '140'), info['formats'][0])

                        st.success("Links gerados com sucesso!")
                        st.subheader("🎥 Vídeo (Direct MP4)")
                        st.code(video_stream['url'])
                        st.subheader("🎵 Áudio (Direct M4A)")
                        st.code(audio_stream['url'])
                except Exception as e:
                    st.error(f"Erro ao extrair links: {e}. Tente outra URL ou verifique o acesso.")

# =======================
# 🎬 MERGE PROFISSIONAL
# =======================
if menu == "🎬 Unir / Otimizar Vídeo":
    st.title("🎬 MediaFusion Engine")
    video_file = st.file_uploader("📹 Upload do vídeo", type=["mp4","webm","mkv"])
    audio_file = st.file_uploader("🎵 Upload do áudio", type=["m4a","mp3","webm"])

    if video_file and audio_file:
        with open("video_input.mp4", "wb") as f: f.write(video_file.getbuffer())
        with open("audio_input.m4a", "wb") as f: f.write(audio_file.getbuffer())

        if st.button("🚀 Processar Vídeo"):
            output_file = "final_output.mp4"
            # Comando eficiente que não re-codifica se não for necessário
            comando = ["ffmpeg", "-y", "-i", "video_input.mp4", "-i", "audio_input.m4a", 
                       "-c", "copy", "-map", "0:v:0", "-map", "1:a:0", output_file]
            
            subprocess.run(comando)
            
            with open(output_file, "rb") as f:
                st.download_button("📥 Baixar Vídeo Final", f, file_name="video_final.mp4")

            # Limpeza
            for f in ["video_input.mp4", "audio_input.m4a", "final_output.mp4"]:
                if os.path.exists(f): os.remove(f)
