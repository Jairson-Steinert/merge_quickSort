"""
Implementação e comparação de algoritmos MergeSort e QuickSort.

Módulo contendo implementações dos algoritmos MergeSort e QuickSort em Python puro,
com medição de performance e geração de arquivos de saída.

Autor: Jairson Steinert  
Curso: Engenharia de Software - Algoritmos Avançados
Instituição: Centro Universitário Católica de Santa Catarina
conjuntos de entrada. Os algoritmos são implementados em Python puro, sem recorrer à rotina de
ordenação interna da linguagem, de modo a permitir uma comparação justa do
desempenho.

Como executar este script:

    python3 merge_quick.py entrada_20000.txt entrada_40000.txt entrada_160000.txt

Cada arquivo de entrada deve conter um inteiro por linha. O script medirá
o tempo necessário para ordenar os números com MergeSort e QuickSort de forma
independente (excluindo a leitura dos arquivos) e exibirá uma tabela
resumida com os resultados.

A implementação de QuickSort utiliza a estratégia de seleção de pivô
“mediana de três” para mitigar o pior caso em dados já ordenados e
atingir um comportamento quase aleatório sem uso de geradores de números
aleatórios. A implementação de MergeSort retorna uma nova lista ordenada em
vez de ordenar no lugar; como o MergeSort requer armazenamento auxiliar,
essa abordagem é clara e fiel à sua implementação típica.
"""

import os
import sys
import time
from typing import List


def merge(left: List[int], right: List[int]) -> List[int]:
    """Mescla duas listas ordenadas em uma única lista ordenada."""
    merged = []
    i = j = 0
    # Mescla até que uma das listas seja esgotada
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    # Adiciona os elementos restantes de qualquer uma das listas
    if i < len(left):
        merged.extend(left[i:])
    if j < len(right):
        merged.extend(right[j:])
    return merged


def mergesort(arr: List[int]) -> List[int]:
    """Implementa o algoritmo MergeSort. Complexidade O(n log n) garantida."""
    n = len(arr)
    if n <= 1:
        return arr.copy()
    mid = n // 2
    left_sorted = mergesort(arr[:mid])
    right_sorted = mergesort(arr[mid:])
    return merge(left_sorted, right_sorted)


def median_of_three(arr: List[int], low: int, high: int) -> int:
    """Retorna o índice da mediana entre arr[low], arr[mid] e arr[high]."""
    mid = (low + high) // 2
    # Cria uma lista de pares (valor, índice) e ordena por valor
    trio = [(arr[low], low), (arr[mid], mid), (arr[high], high)]
    trio.sort(key=lambda x: x[0])
    # O elemento mediano após ordenação estará no índice 1
    return trio[1][1]


def partition(arr: List[int], low: int, high: int) -> int:
    """Particiona array usando esquema de Lomuto com pivô mediana de três."""
    pivot_index = median_of_three(arr, low, high)
    # Move o pivô para o final por conveniência
    arr[pivot_index], arr[high] = arr[high], arr[pivot_index]
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    # Coloca o pivô em sua posição correta na ordenação
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quicksort_recursive(arr: List[int], low: int, high: int) -> None:
    """Implementa QuickSort recursivo in-place com partição de Lomuto."""
    if low < high:
        p = partition(arr, low, high)
        quicksort_recursive(arr, low, p - 1)
        quicksort_recursive(arr, p + 1, high)


def quicksort(arr: List[int]) -> List[int]:
    """Implementa o algoritmo QuickSort. Complexidade O(n log n) médio, O(n²) pior caso."""
    arr_copy = arr.copy()
    quicksort_recursive(arr_copy, 0, len(arr_copy) - 1)
    return arr_copy


def read_integers_from_file(filename: str) -> List[int]:
    """Lê lista de inteiros de um arquivo (um por linha)."""
    # Verificar se arquivo existe
    if not os.path.exists(filename):
        # Sugerir caminho correto se for nome simples
        if '/' not in filename and '\\' not in filename:
            suggested_path = f"dados_entrada/{filename}"
            if os.path.exists(suggested_path):
                print(f"AVISO: Arquivo '{filename}' não encontrado.")
                print(f"SUGESTAO: Você quis dizer: '{suggested_path}'?")
                print(f"USO: python merge_quick.py {suggested_path}")
            else:
                print(f"ERRO: Arquivo '{filename}' não encontrado.")
                print(f"DICA: Verifique se o arquivo está na pasta 'dados_entrada/'")
        raise FileNotFoundError(f"Arquivo não encontrado: {filename}")
    
    with open(filename, 'r') as f:
        return [int(line.strip()) for line in f if line.strip()]


def save_sorted_vector_to_file(vector: List[int], filename: str) -> None:
    """Salva vetor ordenado em arquivo (um número por linha)."""
    import os
    # Criar diretório se não existir
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w') as f:
        for num in vector:
            f.write(f"{num}\n")


def benchmark_sorting_algorithms(filenames: List[str]) -> None:
    """Executa benchmark comparativo entre MergeSort e QuickSort."""
    results = []
    for fname in filenames:
        data = read_integers_from_file(fname)
        n = len(data)
        # Mede o tempo do MergeSort
        arr_for_merge = data.copy()
        start = time.perf_counter()
        merge_result = mergesort(arr_for_merge)
        merge_time = time.perf_counter() - start
        # Mede o tempo do QuickSort
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
        
        print(f"Vetores ordenados salvos:")
        print(f"  MergeSort: {merge_output}")
        print(f"  QuickSort: {quick_output}")
        
        results.append((fname, n, merge_time, quick_time, merge_result, quick_result))

    # Imprime os resultados em uma tabela formatada
    print("=" * 80)
    print("RESUMO DOS RESULTADOS:")
    print("=" * 80)
    print(f"{'Dataset':<17} | {'N':>8} | {'Tempo MergeSort (s)':>20} | {'Tempo QuickSort (s)':>19} | {'Speedup':>8}")
    print("=" * 80)
    
    for fname, n, m_time, q_time, merge_result, quick_result in results:
        speedup = (m_time / q_time - 1) * 100
        dataset_name = fname.replace('dados_entrada/', '').replace('.txt', '')
        
        # Exibe informações de performance
        print(f"{dataset_name:<17} | {n:>8,} | MergeSort: {m_time:.6f} | QuickSort: {q_time:.6f} | Speedup: +{speedup:.1f}%")
    
    print()
    
    # Exibe vetores ordenados retornados após o resumo completo
    print("Vetores Ordenados Retornados:")
    print("=" * 80)
    
    for fname, n, m_time, q_time, merge_result, quick_result in results:
        dataset_name = fname.replace('.txt', '')
        print(f"Dataset: {dataset_name}")
        print(f"  MergeSort: [{', '.join(map(str, merge_result[:10]))}{', ...' if len(merge_result) > 10 else ''}]")
        print(f"  QuickSort: [{', '.join(map(str, quick_result[:10]))}{', ...' if len(quick_result) > 10 else ''}]")
        
        # Verifica se ambos produziram o mesmo resultado (verificação silenciosa)
        if merge_result != quick_result:
            print(f"ERRO: Algoritmos produziram resultados diferentes!")
        print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 merge_quick.py <arquivo_entrada1> [<arquivo_entrada2> ...]")
        sys.exit(1)
    benchmark_sorting_algorithms(sys.argv[1:])