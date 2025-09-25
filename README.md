# Análise Comparativa: MergeSort vs QuickSort

**CENTRO UNIVERSITÁRIO - CATÓLICA DE SANTA CATARINA**  
Engenharia de Software      | Algoritmos Avançados  
Acadêmico: Jairson Steinert | Profa. Ma.: Beatriz Michelson Reichert  


## Estrutura do Projeto

```
merge_quickSort/
├── dados_entrada/                    # Datasets para análise
│   ├── entrada_20000.txt            # Dataset com 20.000 números
│   ├── entrada_40000.txt            # Dataset com 40.000 números
│   └── entrada_160000.txt           # Dataset com 160.000 números
├── merge_quick.py                   # Implementação dos algoritmos principais
├── gera_grafico.py                  # Geração de gráficos comparativos
├── Relatório de Análise - *.pdf     # Relatório final
├── Atividade - Definição.pdf        # Especificação do projeto
├── vetores_ordenados/               # Vetores resultantes (gerados automaticamente)
├── graficos/                        # Gráficos de desempenho (gerados automaticamente)
├── requirements.txt                 # Dependências Python
└── README.md                       # Este arquivo
```

## Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes)

## Instalação

### 1. Clone o Repositório
```bash
git clone https://github.com/Jairson-Steinert/merge_quickSort.git
cd merge_quickSort
```

### 2. Instale as Dependências
```bash
pip install -r requirements.txt
```

## Execução

### Análise Completa (Recomendado)
```bash
# Executa análise em todos os datasets e gera gráfico
python gera_grafico.py
```

### Análise Individual
```bash
# Executa análise em um dataset específico
python merge_quick.py dados_entrada/entrada_20000.txt
python merge_quick.py dados_entrada/entrada_40000.txt 
python merge_quick.py dados_entrada/entrada_160000.txt

# Ou múltiplos datasets
python merge_quick.py dados_entrada/entrada_20000.txt dados_entrada/entrada_40000.txt dados_entrada/entrada_160000.txt
```

## Arquivos Gerados

- **`vetores_ordenados/`**: Vetores ordenados salvos em arquivos texto
  - `Vetor_Ordenado_MergeSort_20000.txt`
  - `Vetor_Ordenado_QuickSort_20000.txt`
  - ... (para cada dataset)

- **`graficos/`**: Gráficos de comparação de desempenho
  - `Grafico_Comparativo_01.png`
  - `Grafico_Comparativo_02.png`
  - ... (numeração automática)

## Algoritmos Implementados

### MergeSort
- **Complexidade**: O(n log n) garantido
- **Estratégia**: Divide e conquista estável
- **Vantagem**: Desempenho consistente e estável

### QuickSort
- **Complexidade**: O(n log n) médio, O(n²) pior caso
- **Estratégia**: Divisão por pivô (mediana de três)
- **Vantagem**: Rápido na prática, baixo overhead

## Saída Esperada

### Tabela Comparativa
```
================================================================================
RESUMO DOS RESULTADOS:
================================================================================
Dataset              |        N |  Tempo MergeSort (s) | Tempo QuickSort (s) |  Speedup
================================================================================
entrada_20000        |   20,000 | MergeSort: 0.030752  | QuickSort: 0.021333 | Speedup: +44.2%
entrada_40000        |   40,000 | MergeSort: 0.061386  | QuickSort: 0.038053 | Speedup: +61.3%
entrada_160000       |  160,000 | MergeSort: 0.335337  | QuickSort: 0.207422 | Speedup: +61.7%

Vetores ordenados salvos em: vetores_ordenados/
```

### Validação dos Vetores Ordenados

| Dataset | Tamanho  | MergeSort | QuickSort  | Verificação |
|---------|----------|-----------|------------|-------------|
| entrada_20000.txt  | 20.000    | ✓ Ordenado | ✓ Ordenado | ✓ Idênticos |
| entrada_40000.txt  | 40.000    | ✓ Ordenado | ✓ Ordenado | ✓ Idênticos |
| entrada_160000.txt | 160.000   | ✓ Ordenado | ✓ Ordenado | ✓ Idênticos |

## Observações Importantes

- **Variação de Desempenho**: Os tempos variarão entre diferentes computadores
- **Foco na Comparação**: O importante é a relação entre os algoritmos, não valores absolutos
- **Implementação Pura**: Algoritmos implementados em Python puro para fins educacionais
- **Pivô Otimizado**: QuickSort usa mediana de três para melhor desempenho médio

## Dependências

- **matplotlib**: Geração de gráficos
- **numpy**: Operações numéricas (opcional, para otimizações)

## Estrutura dos Dados

Os arquivos de entrada contêm números inteiros, um por linha, em ordem aleatória.


## Licença

Este projeto foi desenvolvido para fins educacionais como parte da disciplina de Algoritmos Avançados.
