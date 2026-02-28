import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="YT Pro Downloader", page_icon="⬇️")
st.title("⬇️ YouTube Pro Downloader")

url = st.text_input("Cole a URL do vídeo:")

if st.button("Download em Alta Qualidade"):
    if not url:
        st.warning("Por favor, cole uma URL válida.")
    else:
        with st.spinner("Processando... Isso pode levar alguns instantes (Merge de Vídeo + Áudio)"):
            try:
                # O parâmetro 'best' já seleciona a melhor qualidade disponível
                # sem a necessidade de listar manualmente.
                ydl_opts = {
                    'format': 'bestvideo+bestaudio/best',
                    'merge_output_format': 'mp4',
                    'outtmpl': 'video_final.mp4',
                    'quiet': True,
                    'no_warnings': True,
                    'postprocessors': [{
                        'key': 'FFmpegVideoConvertor',
                        'preferedformat': 'mp4',
                    }],
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                # Verifica se o arquivo foi criado
                if os.path.exists("video_final.mp4"):
                    with open("video_final.mp4", "rb") as f:
                        st.download_button(
                            label="📥 Baixar Vídeo (Alta Qualidade)",
                            data=f,
                            file_name="video_alta_qualidade.mp4",
                            mime="video/mp4"
                        )
                    st.success("Download pronto!")
                else:
                    st.error("Erro: O arquivo não foi gerado.")
            
            except Exception as e:
                st.error(f"Erro ao processar o vídeo: {e}")

# Limpeza automática de arquivos antigos ao recarregar a página
if os.path.exists("video_final.mp4"):
    os.remove("video_final.mp4")
