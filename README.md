# 🧵 Atividade 4: Paralelização de Processamento (Caixa-Preta)

# 📌 Sobre o Projeto
# Este projeto faz parte da disciplina de Sistemas Concorrentes e Distribuídos.
# O desafio consiste em paralelizar a conversão de uma imagem de 16GB para escala de cinza,
# tratando o script original como uma caixa-preta (sem alterar nenhuma linha do conversor).

# --------------------------------------------------

# 👥 Regras da Atividade
# - Formação: Grupo de 4 alunos
# - Repositório: Realizar fork do projeto original
# - Colaboração: Adicionar membros como colaboradores
# - Restrição: NÃO modificar conversoremescalacinza.py

# --------------------------------------------------

# 🛠️ Tecnologias Utilizadas
# - Python 3.10+
# - PowerShell / Bash
# - Multiprocessing (externo via SO)

# --------------------------------------------------

# 🚀 Fluxo de Trabalho

# 1️⃣ Geração da Imagem Base (executar apenas uma vez)
python .\geradorimagem.py

# --------------------------------------------------

# 2️⃣ Execução Serial (baseline)
python .\conversoremescalacinza.py imagem_aleatoria_1gb.ppm saida_serial.ppm

# Resultado esperado:
# ✅ Processamento concluído!
# ⏱️ Tempo total: 167.13 segundos

# --------------------------------------------------

# 3️⃣ Estratégia de Paralelização
# - Dividir a imagem em partes (fatias horizontais)
# - Executar múltiplos processos em paralelo
# - Aguardar conclusão
# - Reunir as partes no final

# --------------------------------------------------

# 📊 Resultados do Experimento
# Configuração        Tempo (s)     Speedup
# Serial              167.13        1.0x
# 2 Threads           86.45         ~1.93x
# 4 Threads           45.12         ~3.70x
# 8 Threads           24.80         ~6.73x
# 12 Threads          19.35         ~8.63x

# --------------------------------------------------

# 🖥️ Como Executar a Solução

# 2 threads
python paralelizar.py 2

# 4 threads
python paralelizar.py 4

# 8 threads
python paralelizar.py 8

# 12 threads
python paralelizar.py 12

# --------------------------------------------------

# 💡 Observações Técnicas
# - Ganho não linear devido a gargalos de I/O
# - Limitação de CPU (núcleos físicos)
# - Aumento de uso de RAM conforme threads
# - Overhead de múltiplos processos

# --------------------------------------------------

# 👨‍💻 Grupo de Trabalho
# - Ana Júlia de Almeida Machado
# - Samuel de Souza
# - Vinicius Caetano de Assis


# --------------------------------------------------

# © 2026 Atividade de Computação Concorrente - Unieuro
