import streamlit as st
import yt_dlp

st.set_page_config(page_title="YT Downloader Pro", layout="centered")

st.title("📥 YouTube Downloader - Seletor de Qualidade")

url = st.text_input("Cole a URL do vídeo:")


def listar_formatos(url):
    ydl_opts = {
        "quiet": True,
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        formatos = []
        for f in info["formats"]:
            if f.get("vcodec") != "none":  # apenas formatos com vídeo
                formatos.append({
                    "format_id": f["format_id"],
                    "resolucao": f.get("resolution", "N/A"),
                    "ext": f["ext"],
                    "filesize": f.get("filesize")
                })

        return info["title"], formatos


def pegar_link(url, format_id):
    ydl_opts = {
        "quiet": True,
        "format": format_id,
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info["url"]


if st.button("Buscar Qualidades"):
    if url:
        with st.spinner("Buscando formatos disponíveis..."):
            try:
                titulo, formatos = listar_formatos(url)
                st.session_state["formatos"] = formatos
                st.session_state["titulo"] = titulo
                st.success("Qualidades encontradas!")
            except Exception as e:
                st.error(f"Erro: {e}")
    else:
        st.warning("Insira uma URL.")


if "formatos" in st.session_state:
    st.subheader(f"🎬 {st.session_state['titulo']}")

    opcoes = {
        f"{f['resolucao']} - {f['ext']} (id: {f['format_id']})": f["format_id"]
        for f in st.session_state["formatos"]
    }

    escolha = st.selectbox("Escolha a qualidade:", list(opcoes.keys()))

    if st.button("Gerar Link de Download"):
        format_id = opcoes[escolha]
        link = pegar_link(url, format_id)
        st.success("Link gerado!")
        st.markdown(f"[Clique aqui para baixar]({link})")