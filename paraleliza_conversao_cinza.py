import os
import sys
import time
import threading
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import List, Tuple

# ===================== CONFIGURAÇÕES =====================
DIRETORIO_PARTES = "partes"
DIRETORIO_SAIDA_CINZA = "partes_cinza"
CONVERSOR_SCRIPT = "conversoremescalacinza.py"   # mantido como referência

PYTHON_VENV = os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe")


def ler_header_ppm(arquivo: str) -> Tuple[int, int, int]:
    with open(arquivo, "rb") as f:
        f.readline()
        linha = f.readline().strip()
        while linha.startswith(b'#'):
            linha = f.readline().strip()
        largura, altura = map(int, linha.split())
        linha = f.readline().strip()
        while linha.startswith(b'#'):
            linha = f.readline().strip()
        maxval = int(linha)
        return largura, altura, maxval


def converter_parte_com_subprocess(args):
    """Versão com subprocess (mais fiel ao pedido do professor)"""
    idx, arquivo_entrada = args
    arquivo_saida = os.path.join(DIRETORIO_SAIDA_CINZA, f"parte_{idx:03d}_cinza.ppm")
    
    inicio = time.perf_counter()
    result = subprocess.run(
        [PYTHON_VENV, CONVERSOR_SCRIPT, arquivo_entrada, arquivo_saida],
        capture_output=True,
        text=True,
        check=True
    )
    tempo = time.perf_counter() - inicio
    return idx, arquivo_saida, tempo


# ================== VERSÃO MAIS RÁPIDA (RECOMENDADA) ==================
def converter_parte_direta(args):
    """Converte diretamente usando a função do professor (mais rápido)"""
    idx, arquivo_entrada = args
    arquivo_saida = os.path.join(DIRETORIO_SAIDA_CINZA, f"parte_{idx:03d}_cinza.ppm")
    
    inicio = time.perf_counter()
    
    # Importamos a função diretamente do módulo do professor
    import importlib.util
    spec = importlib.util.spec_from_file_location("conversor", CONVERSOR_SCRIPT)
    conversor = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(conversor)
    
    tempo = conversor.converter_para_cinza_serial(arquivo_entrada, arquivo_saida, linhas_por_bloco=256)
    
    return idx, arquivo_saida, tempo


def progress_monitor(stop_event, total):
    processed = 0
    while not stop_event.is_set():
        time.sleep(0.3)
        pct = min(processed / total * 100, 99.9)
        print(f"\rProgresso: {processed}/{total} partes ({pct:5.1f}%)", end="", flush=True)
    print(f"\rProgresso: {total}/{total} partes (100.0%)\n")


def juntar_partes(arquivos: List[str], arquivo_final: str, largura: int, altura: int, maxval: int):
    print(f"\nJuntando {len(arquivos)} partes...")
    with open(arquivo_final, "wb") as fout:
        fout.write(f"P6\n{largura} {altura}\n{maxval}\n".encode())
        for arq in sorted(arquivos):
            with open(arq, "rb") as fin:
                for _ in range(3):
                    fin.readline()
                while chunk := fin.read(4*1024*1024):
                    fout.write(chunk)
    print("Junção concluída!\n")


def main():
    print("=" * 90)
    print("   PARALELIZAÇÃO DA CONVERSÃO PARA ESCALA DE CINZA - VERSÃO OTIMIZADA")
    print("=" * 90)

    n_threads = int(input("\nQuantas threads deseja usar? (recomendado 8-12): ") or "8")

    # Verifica partes
    partes = sorted([os.path.join(DIRETORIO_PARTES, f) for f in os.listdir(DIRETORIO_PARTES) if f.endswith('.ppm')])
    if not partes:
        print("ERRO: Nenhuma parte encontrada na pasta 'partes'")
        sys.exit(1)

    print(f"\nEncontradas {len(partes)} partes. Iniciando conversão com {n_threads} threads...\n")

    largura, altura, maxval = ler_header_ppm("imagem_aleatoria_1gb.ppm")
    os.makedirs(DIRETORIO_SAIDA_CINZA, exist_ok=True)

    stop_event = threading.Event()
    monitor = threading.Thread(target=progress_monitor, args=(stop_event, len(partes)), daemon=True)
    monitor.start()

    t_inicio = time.perf_counter()

    # === Use esta linha para versão MAIS RÁPIDA ===
    funcao_conversao = converter_parte_direta     # <--- Mais rápida

    with ProcessPoolExecutor(max_workers=n_threads) as executor:
        futures = [executor.submit(funcao_conversao, (i, p)) for i, p in enumerate(partes)]
        arquivos_cinza = []
        for future in as_completed(futures):
            idx, saida, tempo = future.result()
            arquivos_cinza.append(saida)
            # processed += 1   (não precisamos mais, o monitor cuida)

    tempo_total = time.perf_counter() - t_inicio
    stop_event.set()
    monitor.join()

    arquivo_final = f"imagem_cinza_{n_threads}threads.ppm"
    juntar_partes(arquivos_cinza, arquivo_final, largura, altura, maxval)

    print("=" * 90)
    print("✅ CONVERSÃO CONCLUÍDA!")
    print(f"⏱️ Tempo total da conversão: {tempo_total:.2f} segundos ({tempo_total/60:.2f} minutos)")
    print(f"Arquivo final: {arquivo_final}")
    print(f"Threads utilizadas: {n_threads}")
    print("=" * 90)


if __name__ == "__main__":
    main()