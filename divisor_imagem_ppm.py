import os
import sys
from typing import List, Tuple

def ler_header_ppm(arquivo: str) -> tuple[int, int, int, int]:
    """Lê o header do PPM e retorna (largura, altura, maxval, offset_dados)"""
    with open(arquivo, "rb") as f:
        tipo = f.readline().strip()
        if tipo != b'P6':
            raise ValueError("Formato não suportado. Esperado PPM P6.")

        linha = f.readline().strip()
        while linha.startswith(b'#'):
            linha = f.readline().strip()

        largura, altura = map(int, linha.split())

        linha = f.readline().strip()
        while linha.startswith(b'#'):
            linha = f.readline().strip()

        valor_maximo = int(linha)
        offset_dados = f.tell()
        return largura, altura, valor_maximo, offset_dados


def dividir_imagem_ppm(
    arquivo_entrada: str,
    n_partes: int,
    diretorio_saida: str = "partes"
) -> List[str]:
    """
    Divide o arquivo PPM em N partes menores, cada uma sendo um PPM válido.
    Retorna a lista de caminhos dos arquivos gerados.
    """
    if not os.path.isfile(arquivo_entrada):
        raise FileNotFoundError(f"Arquivo não encontrado: {arquivo_entrada}")

    largura, altura, maxval, offset_dados = ler_header_ppm(arquivo_entrada)
    
    print(f"Dividindo imagem {largura}x{altura} em {n_partes} partes...")

    os.makedirs(diretorio_saida, exist_ok=True)

    linhas_por_parte = (altura + n_partes - 1) // n_partes
    arquivos_gerados: List[str] = []

    with open(arquivo_entrada, "rb") as fin:
        fin.seek(offset_dados)
        dados_pixels = fin.read()  # lê todos os dados (16GB → cuidado com memória, mas ok para esta atividade)

    for i in range(n_partes):
        inicio_linha = i * linhas_por_parte
        fim_linha = min(inicio_linha + linhas_por_parte, altura)
        
        if inicio_linha >= altura:
            break

        bloco_altura = fim_linha - inicio_linha
        bytes_inicio = inicio_linha * largura * 3
        bytes_fim = fim_linha * largura * 3

        bloco_dados = dados_pixels[bytes_inicio:bytes_fim]

        # Cria header para esta parte
        header = f"P6\n{largura} {bloco_altura}\n{maxval}\n".encode("ascii")

        nome_saida = os.path.join(diretorio_saida, f"parte_{i:03d}.ppm")
        with open(nome_saida, "wb") as fout:
            fout.write(header)
            fout.write(bloco_dados)

        arquivos_gerados.append(nome_saida)
        print(f"  → Parte {i+1}/{n_partes}: {bloco_altura} linhas → {nome_saida}")

    print(f"Divisão concluída! {len(arquivos_gerados)} partes criadas em '{diretorio_saida}'/\n")
    return arquivos_gerados


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python divisor_imagem_ppm.py <arquivo_entrada> [n_partes]")
        sys.exit(1)

    entrada = sys.argv[1]
    n_partes = int(sys.argv[2]) if len(sys.argv) > 2 else 8

    dividir_imagem_ppm(entrada, n_partes)