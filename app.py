import streamlit as st
import yt_dlp
import subprocess
import os
import shutil
import json
from pathlib import Path

st.set_page_config(
    page_title="MediaFusion Pro",
    layout="wide",
    page_icon="🚀"
)

# =======================
# 🎨 UI SaaS Premium
# =======================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}
section[data-testid="stSidebar"] {
    background: #111827;
}
.stButton>button, .stDownloadButton>button {
    width: 100%;
    border-radius: 12px;
    height: 50px;
    font-size: 16px;
    font-weight: bold;
}
h1, h2, h3 { text-align: center; }
</style>
""", unsafe_allow_html=True)

# =======================
# 🔥 MENU
# =======================
menu = st.sidebar.radio(
    "📂 Menu",
    ["🔗 Gerar Links", "🎬 Unir / Otimizar Vídeo"]
)

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
                    ydl_opts = {
                        'quiet': True,
                        'format': 'bestvideo+bestaudio/best',
                    }

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=False)

                        video_url = info['url']

                        ydl_opts['format'] = 'bestaudio'
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl_audio:
                            info_audio = ydl_audio.extract_info(url, download=False)
                            audio_url = info_audio['url']

                    st.success("Links gerados!")

                    st.subheader("🎥 Vídeo")
                    st.code(video_url)

                    st.subheader("🎵 Áudio")
                    st.code(audio_url)

                except Exception as e:
                    st.error(str(e))

# =======================
# 🎬 MERGE PROFISSIONAL
# =======================
if menu == "🎬 Unir / Otimizar Vídeo":

    st.title("🎬 MediaFusion Engine")

    video_file = st.file_uploader("📹 Upload do vídeo", type=["mp4","webm","mkv"])
    audio_file = st.file_uploader("🎵 Upload do áudio", type=["m4a","mp3","webm"])

    def get_media_info(file):
        result = subprocess.run(
            ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", file],
            capture_output=True,
            text=True
        )
        return json.loads(result.stdout)

    if video_file and audio_file:

        with open("video_input", "wb") as f:
            shutil.copyfileobj(video_file, f)

        with open("audio_input", "wb") as f:
            shutil.copyfileobj(audio_file, f)

        video_info = get_media_info("video_input")
        duration = float(video_info["format"]["duration"])
        size_mb = int(video_info["format"]["size"]) / (1024*1024)

        st.info(f"⏱ Duração: {round(duration,2)}s | 📦 Tamanho: {round(size_mb,2)} MB")

        compress = False
        if size_mb > 800:
            st.warning("Arquivo grande detectado. Compressão inteligente ativada.")
            compress = True

        if st.button("🚀 Processar Vídeo"):

            progress = st.progress(0)
            status = st.empty()

            output_file = "final_output.mp4"

            if compress:
                comando = [
                    "ffmpeg",
                    "-i","video_input",
                    "-i","audio_input",
                    "-map","0:v:0",
                    "-map","1:a:0",
                    "-c:v","libx264",
                    "-preset","fast",
                    "-crf","23",
                    "-c:a","aac",
                    "-movflags","+faststart",
                    output_file
                ]
            else:
                comando = [
                    "ffmpeg",
                    "-i","video_input",
                    "-i","audio_input",
                    "-map","0:v:0",
                    "-map","1:a:0",
                    "-c","copy",
                    "-movflags","+faststart",
                    output_file
                ]

            process = subprocess.Popen(
                comando,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            for line in process.stderr:
                if "time=" in line:
                    try:
                        time_str = line.split("time=")[1].split(" ")[0]
                        h, m, s = time_str.split(":")
                        current = float(h)*3600 + float(m)*60 + float(s)
                        percent = min(current/duration,1.0)
                        progress.progress(percent)
                        status.text(f"Processando... {int(percent*100)}%")
                    except:
                        pass

            process.wait()
            progress.progress(1.0)
            status.text("Finalizado!")

            if Path(output_file).exists():
                with open(output_file,"rb") as f:
                    st.download_button(
                        "📥 Baixar Vídeo Final",
                        f,
                        file_name="video_final.mp4",
                        mime="video/mp4"
                    )

            # limpeza
            for file in ["video_input","audio_input","final_output.mp4"]:
                if os.path.exists(file):
                    os.remove(file)
