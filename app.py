import streamlit as st
import os
import requests
import asyncio
from editor import processar_video_completo, gerar_voz_antonio

# Configuração de Elite
st.set_page_config(page_title="Máquina Viral v2", layout="wide")
st.title("🎬 Fábrica de Conteúdo: Motor NewPipe")

if "video_selecionado" not in st.session_state:
    st.session_state.video_selecionado = None
if "resultados" not in st.session_state:
    st.session_state.resultados = []

# --- FASE 1: BUSCA VIA NEWPIPE/PIPED ---
if not st.session_state.video_selecionado:
    st.subheader("🔍 Localizar Alvo Real (Motor NewPipe)")
    busca = st.text_input("Qual o produto do bilhão hoje, Mestre?", placeholder="Ex: Mini Selador de Embalagens")
    
    if st.button("🔎 Pesquisar Alvos"):
        with st.spinner("Infiltrando no banco de dados do NewPipe..."):
            # Usando a API pública do Piped (NewPipe Backend)
            url_api = f"https://pipedapi.kavin.rocks/search?q={busca}&filter=videos"
            try:
                response = requests.get(url_api)
                dados = response.json()
                
                # Captura os 3 primeiros vídeos reais
                st.session_state.resultados = []
                for item in dados['items'][:3]:
                    st.session_state.resultados.append({
                        "id": item['url'].split("=")[-1],
                        "url": f"https://www.youtube.com/watch?v={item['url'].split('=')[-1]}",
                        "title": item['title'],
                        "thumb": item['thumbnail']
                    })
            except Exception as e:
                st.error(f"Erro na conexão com NewPipe: {e}")

    if st.session_state.resultados:
        st.write("### 🎯 Alvos Encontrados")
        cols = st.columns(len(st.session_state.resultados))
        for idx, v in enumerate(st.session_state.resultados):
            with cols[idx]:
                st.image(v['thumb'], use_container_width=True)
                st.write(f"**{v['title'][:40]}...**")
                if st.button(f"🎯 CAPTURAR {v['id']}", key=f"btn_{v['id']}"):
                    st.session_state.video_selecionado = v['url']
                    st.rerun()

# --- FASE 2: EDIÇÃO (Aqui o Antônio assume) ---
else:
    st.sidebar.success("💎 ALVO EM CUSTÓDIA")
    if st.sidebar.button("❌ TROCAR ALVO"):
        st.session_state.video_selecionado = None
        st.rerun()
    
    st.info(f"Editando Alvo: {st.session_state.video_selecionado}")
    # [O restante do seu código de edição continua aqui...]