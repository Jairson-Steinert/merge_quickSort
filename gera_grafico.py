"""
Gerador de gráficos comparativos para algoritmos de ordenação.

Executa análise completa dos algoritmos MergeSort e QuickSort,
gera gráficos comparativos e salva resultados ordenados.

Autor: Jairson Steinert  
Curso: Engenharia de Software - Algoritmos Avançados
Instituição: Centro Universitário Católica de Santa Catarina
"""

import matplotlib.pyplot as plt
import numpy as np
import time
import os
import glob
from typing import List, Tuple

# Importar as funções do merge_quick.py
from merge_quick import (
    mergesort, 
    quicksort, 
    read_integers_from_file,
    save_sorted_vector_to_file
)


def get_next_filename(base_name: str, extension: str = ".png") -> str:
    """
    Gera o próximo nome de arquivo sequencial.
    
    Parâmetros:
    -----------
    base_name : str
        Nome base do arquivo (ex: "Grafico_Comparativo")
    extension : str
        Extensão do arquivo (ex: ".png")
        
    Retorna:
    --------
    str
        Próximo nome disponível (ex: "graficos/Grafico_Comparativo_01.png")
    """
    # Criar diretório se não existir
    os.makedirs("graficos", exist_ok=True)
    
    # Procurar por arquivos existentes com o padrão
    pattern = f"graficos/{base_name}_*{extension}"
    existing_files = glob.glob(pattern)
    
    # Também verificar arquivos sem numeração (caso base)
    base_file = f"graficos/{base_name}{extension}"
    if os.path.exists(base_file):
        existing_files.append(base_file)
    
    if not existing_files:
        # Se não há arquivos, começar com 01
        return f"graficos/{base_name}_01{extension}"
    
    # Extrair números dos arquivos existentes
    numbers = []
    for file in existing_files:
        filename = os.path.basename(file)
        if filename == f"{base_name}{extension}":
            # Arquivo original sem número (considerar como 00)
            numbers.append(0)
        else:
            try:
                # Extrair número entre último _ e extensão
                name_without_ext = filename.replace(extension, "")
                if "_" in name_without_ext:
                    num_str = name_without_ext.split("_")[-1]
                    numbers.append(int(num_str))
            except ValueError:
                continue
    
    # Próximo número sequencial
    next_num = max(numbers) + 1 if numbers else 1
    return f"graficos/{base_name}_{next_num:02d}{extension}"


def benchmark_and_plot(filenames: List[str]) -> None:
    """
    Executa benchmark dos algoritmos e gera gráfico comparativo.
    
    Parâmetros
    ----------
    filenames : List[str]
        Lista de arquivos de entrada para teste
    """
    
    # Coletar dados
    file_labels = []
    sizes = []
    merge_times = []
    quick_times = []
    
    print("Executando benchmarks...")
    
    for fname in filenames:
        print(f"Processando {fname}...")
        
        # Ler dados
        data = read_integers_from_file(fname)
        n = len(data)
        
        # Benchmark MergeSort
        arr_for_merge = data.copy()
        start = time.perf_counter()
        merge_result = mergesort(arr_for_merge)
        merge_time = time.perf_counter() - start
        
        # Benchmark QuickSort
        arr_for_quick = data.copy()
        start = time.perf_counter()
        quick_result = quicksort(arr_for_quick)
        quick_time = time.perf_counter() - start
        
        # Salvar vetores ordenados em arquivos com nova nomenclatura
        base_name = fname.replace('dados_entrada/', '').replace('.txt', '')
        size_str = base_name.replace('entrada_', '')
        
        merge_output = f"vetores_ordenados/Vetor_Ordenado_MergeSort_{size_str}.txt"
        quick_output = f"vetores_ordenados/Vetor_Ordenado_QuickSort_{size_str}.txt"
        
        save_sorted_vector_to_file(merge_result, merge_output)
        save_sorted_vector_to_file(quick_result, quick_output)
        
        print(f"  Vetores ordenados salvos:")
        print(f"    MergeSort: {merge_output}")
        print(f"    QuickSort: {quick_output}")
        
        # Armazenar resultados
        file_labels.append(fname.replace('.txt', '').replace('entrada_', ''))
        sizes.append(n)
        merge_times.append(merge_time)
        quick_times.append(quick_time)
        
        # Armazenar dados para exibição posterior
        results_data = getattr(benchmark_and_plot, 'results_data', [])
        results_data.append((fname, n, merge_time, quick_time, merge_result, quick_result))
        benchmark_and_plot.results_data = results_data
    
    # Mostrar resumo dos tempos de execução
    print("=" * 80)
    print("Resumo dos Resultados:")
    print("=" * 80)
    print(f"{'Dataset':<20} | {'N':>8} | {'Tempo MergeSort (s)':>20} | {'Tempo QuickSort (s)':>19} | {'Speedup':>8}")
    print("=" * 80)
    
    for i, (fname, n, merge_time, quick_time, merge_result, quick_result) in enumerate(benchmark_and_plot.results_data):
        speedup = (merge_time / quick_time - 1) * 100
        dataset_name = fname.replace('.txt', '')
        print(f"{dataset_name:<20} | {n:>8,} | MergeSort: {merge_time:.6f} | QuickSort: {quick_time:.6f} | Speedup: +{speedup:.1f}%")
    
    print()
    
    # Exibir vetores ordenados retornados após o resumo completo
    print("Vetores Ordenados Retornados:")
    print("=" * 80)
    
    for fname, n, merge_time, quick_time, merge_result, quick_result in benchmark_and_plot.results_data:
        dataset_name = fname.replace('.txt', '')
        print(f"Dataset: {dataset_name}")
        print(f"  MergeSort: [{', '.join(map(str, merge_result[:10]))}{', ...' if len(merge_result) > 10 else ''}]")
        print(f"  QuickSort: [{', '.join(map(str, quick_result[:10]))}{', ...' if len(quick_result) > 10 else ''}]")
        
        # Verificar se ambos produziram o mesmo resultado (verificação silenciosa)
        if merge_result != quick_result:
            print(f"ERRO: Algoritmos produziram resultados diferentes!")
        print()
    
    # Criar gráfico
    filename = create_comparison_plot(file_labels, sizes, merge_times, quick_times)
    
    return sizes, merge_times, quick_times, filename


def create_comparison_plot(labels: List[str], sizes: List[int], 
                         merge_times: List[float], quick_times: List[float]) -> None:
    """
    Cria gráfico comparativo dos tempos de execução.
    """
    
    # Configurar estilo
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Posições das barras
    x_pos = np.arange(len(labels))
    width = 0.35
    
    # Criar barras
    bars1 = ax.bar(x_pos - width/2, merge_times, width, 
                   label='MergeSort', color="#0b6158", alpha=0.8)
    bars2 = ax.bar(x_pos + width/2, quick_times, width,
                   label='QuickSort', color="#aad196", alpha=0.8)
    
    # Configurar eixos e título
    ax.set_xlabel('Dataset (Número de Elementos)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Tempo de Execução (segundos)', fontsize=14, fontweight='bold')
    ax.set_title('Comparação de Desempenho: MergeSort vs QuickSort', 
                 fontsize=16, fontweight='bold', pad=20)
    
    # Configurar eixo X
    ax.set_xticks(x_pos)
    ax.set_xticklabels([f"{label}\n({sizes[i]:,} elementos)" 
                        for i, label in enumerate(labels)], fontsize=11)
    
    # Adicionar valores nas barras
    def add_value_labels(bars):
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.4f}s',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),  # 3 points vertical offset
                       textcoords="offset points",
                       ha='center', va='bottom',
                       fontsize=10, fontweight='bold')
    
    add_value_labels(bars1)
    add_value_labels(bars2)
    
    # Configurar legenda
    ax.legend(loc='upper left', fontsize=12, framealpha=0.9)
    
    # Configurar grid
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    # Ajustar layout
    plt.tight_layout()
    
    # Gerar nome sequencial para arquivo
    filename = get_next_filename("Grafico_Comparativo")
    
    # Salvar gráfico
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"\nGráfico salvo como '{filename}'")
    
    plt.show() # Descomente se quiser mostrar o gráfico
    
    return filename


def main():
    """Função principal do script."""
    
    # Arquivos de entrada
    input_files = [
        'dados_entrada/entrada_20000.txt',
        'dados_entrada/entrada_40000.txt', 
        'dados_entrada/entrada_160000.txt'
    ]
    
    print("=" * 60)
    print("GERADOR DE GRÁFICO COMPARATIVO")
    print("MergeSort vs QuickSort")
    print("=" * 60)
    
    # Executar benchmark e gerar plot
    sizes, merge_times, quick_times, filename = benchmark_and_plot(input_files)
    
    print(f"\nGráfico salvo como '{filename}'")


if __name__ == "__main__":
    main()