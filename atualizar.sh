#!/bin/bash
# Puxa o código novo do GitHub
git pull origin main

# Mata processos antigos para liberar a porta 8501
sudo fuser -k 8501/tcp
sudo pkill -9 -f streamlit

# Ativa o motor e lança a máquina
source venv/bin/activate
nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 > logs_maquina.txt 2>&1 &

echo "🚀 Máquina Viral Atualizada e Online na Nuvem, Mestre!"
