import streamlit as st
import yt_dlp
import subprocess
import os
import requests

st.set_page_config(page_title="MediaFusion Pro", layout="wide", page_icon="🚀")

# =======================
# CSS Premium
# =======================
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); color: white; }
.stButton>button { border-radius: 12px; height: 50px; font-weight: bold; }
.stTextInput>div>input { height: 40px; border-radius: 8px; padding: 5px; }
</style>
""", unsafe_allow_html=True)

menu = st.sidebar.radio("📂 Menu", ["🔗 Gerar Links", "🎬 Unir / Otimizar Vídeo"])

# =======================
# 🔗 GERADOR DE LINKS
# =======================
if menu == "🔗 Gerar Links":
    st.title("🔗 Gerador de Links Diretos")
    url = st.text_input("Cole a URL do vídeo (YouTube ou suportado):")

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

                        # Converter generators em listas
                        video_formats = list(ydl.build_format_selector('bestvideo')(info))
                        audio_formats = list(ydl.build_format_selector('bestaudio')(info))

                        video_stream = video_formats[0] if video_formats else None
                        audio_stream = audio_formats[0] if audio_formats else None

                        if video_stream:
                            st.success(f"Qualidade detectada: {video_stream.get('resolution', 'N/A')}")
                            st.subheader("🎥 Vídeo (Direct Stream)")
                            st.code(video_stream['url'])
                        else:
                            st.warning("Não foi possível detectar o vídeo.")

                        if audio_stream:
                            st.subheader("🎵 Áudio (Direct Stream)")
                            st.code(audio_stream['url'])
                        else:
                            st.warning("Não foi possível detectar o áudio.")

                        st.info("⚠️ Você pode copiar esses links para o menu 'Unir / Otimizar' para fazer o merge sem precisar baixar manualmente.")
                except Exception as e:
                    st.error(f"Erro ao extrair links: {e}")
        else:
            st.warning("Por favor, insira uma URL válida.")

# =======================
# 🎬 MERGE PROFISSIONAL
# =======================
if menu == "🎬 Unir / Otimizar Vídeo":
    st.title("🎬 MediaFusion Engine")

    st.subheader("Opção 1: Upload de arquivos")
    video_file = st.file_uploader("📹 Upload do vídeo (sem áudio)", type=["mp4","webm","mkv"])
    audio_file = st.file_uploader("🎵 Upload do áudio", type=["m4a","mp3","webm"])

    st.subheader("Opção 2: Colar links diretos")
    video_link = st.text_input("📹 Cole o link direto do vídeo (MP4/WebM)")
    audio_link = st.text_input("🎵 Cole o link direto do áudio (M4A/MP3/WebM)")

    ready_to_merge = False
    video_input_path = "video_input.tmp"
    audio_input_path = "audio_input.tmp"

    # -----------------------
    # Preparar arquivos do upload
    # -----------------------
    if video_file and audio_file:
        with open(video_input_path, "wb") as f:
            f.write(video_file.getbuffer())
        with open(audio_input_path, "wb") as f:
            f.write(audio_file.getbuffer())
        ready_to_merge = True

    # -----------------------
    # Preparar arquivos dos links diretos
    # -----------------------
    elif video_link and audio_link:
        try:
            with st.spinner("Baixando arquivos dos links..."):
                video_data = requests.get(video_link)
                audio_data = requests.get(audio_link)

                if video_data.status_code == 200 and audio_data.status_code == 200:
                    with open(video_input_path, "wb") as f:
                        f.write(video_data.content)
                    with open(audio_input_path, "wb") as f:
                        f.write(audio_data.content)
                    ready_to_merge = True
                else:
                    st.error("Falha ao baixar os arquivos. Verifique os links.")
        except Exception as e:
            st.error(f"Erro ao baixar arquivos: {e}")

    # -----------------------
    # Merge com FFmpeg
    # -----------------------
    if ready_to_merge and st.button("🚀 Processar e Unir"):
        output_file = "video_final.mp4"
        comando = [
            "ffmpeg", "-y",
            "-i", video_input_path,
            "-i", audio_input_path,
            "-c", "copy",
            "-map", "0:v:0",
            "-map", "1:a:0",
            output_file
        ]
        with st.spinner("Realizando o Merge (MUX) de alta velocidade..."):
            try:
                subprocess.run(comando, check=True)
                if os.path.exists(output_file):
                    with open(output_file, "rb") as f:
                        st.download_button("📥 Baixar Vídeo Final", f, file_name="video_final.mp4")
                    st.success("✅ Merge concluído com sucesso!")
            except subprocess.CalledProcessError as e:
                st.error(f"Erro ao processar o vídeo: {e}")
            finally:
                # Limpeza
                for f in [video_input_path, audio_input_path, output_file]:
                    if os.path.exists(f):
                        os.remove(f)
