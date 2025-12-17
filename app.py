import streamlit as st
import os
from editor import processar_video

# Configuração da Página
st.set_page_config(page_title="Fábrica de Vídeos v2", layout="wide")

st.title("🎬 Fábrica de Vídeos - Controle Total")

# Caminhos das pastas (Ajustados para a estrutura da sua VPS)
PASTA_ENTRADA = "videos_originais"
PASTA_SAIDA = "videos_finalizados"

# Cria as pastas caso não existam
for pasta in [PASTA_ENTRADA, PASTA_SAIDA]:
    if not os.path.exists(pasta):
        os.makedirs(pasta)

# --- BARRA LATERAL ---
st.sidebar.header("Configurações de Busca")
filtro_produto = st.sidebar.text_input("🔍 Nome do Produto (ou parte do arquivo):", "")

# Listar arquivos que batem com o filtro
todos_arquivos = os.listdir(PASTA_ENTRADA)
arquivos_filtrados = [f for f in todos_arquivos if filtro_produto.lower() in f.lower() and f.endswith(('.mp4', '.mov'))]

st.sidebar.write(f"Encontrados: {len(arquivos_filtrados)} vídeos")

# --- ÁREA PRINCIPAL ---
if arquivos_filtrados:
    video_selecionado = st.selectbox("Selecione o vídeo para editar:", arquivos_filtrados)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("Pré-visualização do Original")
        st.video(os.path.join(PASTA_ENTRADA, video_selecionado))
        
    with col2:
        texto_overlay = st.text_input("Texto para o vídeo:", value=filtro_produto)
        cor_texto = st.color_picker("Cor do texto:", "#FFFFFF")
        
        if st.button("🚀 Gerar Vídeo Final"):
            with st.spinner("Processando... Isso pode levar alguns minutos na VPS."):
                caminho_entrada = os.path.join(PASTA_ENTRADA, video_selecionado)
                nome_saida = f"final_{video_selecionado}"
                caminho_saida = os.path.join(PASTA_SAIDA, nome_saida)
                
                sucesso, mensagem = processar_video(caminho_entrada, caminho_saida, texto_overlay, cor_texto)
                
                if sucesso:
                    st.success(f"Vídeo pronto: {nome_saida}")
                    st.video(caminho_saida)
                    with open(caminho_saida, "rb") as file:
                        st.download_button("⬇️ Baixar Vídeo", data=file, file_name=nome_saida)
                else:
                    st.error(f"Erro no processamento: {mensagem}")
else:
    st.warning("Nenhum vídeo encontrado com esse nome na pasta 'videos_originais'.")