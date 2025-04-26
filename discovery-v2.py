import pandas as pd
import matplotlib.pyplot as plt
import pm4py
from pm4py.algo.discovery.dfg import algorithm as dfg_algorithm
from pm4py.visualization.dfg import visualizer as dfg_visualizer

def alinhamento_heuristico(data):
    # Inicialização das estruturas de dados
    processos = {}

    # Loop para construir os processos
    for caseid, atividade in data.groupby(data.columns[0])['activity']:
        processo = '-'.join(atividade.tolist())  # Modificação aqui
        processos[processo] = processos.get(processo, 0) + 1

    return processos

def plotar_grafico(processos, top_n=5):
    # Ordena os processos pela frequência
    processos_ordenados = sorted(processos.items(), key=lambda x: x[1], reverse=True)[:top_n]

    # Extrai as atividades principais e suas frequências
    atividades_principais = [processo[0] for processo in processos_ordenados]
    frequencias = [processo[1] for processo in processos_ordenados]

    # Plota o gráfico de barras
    plt.figure(figsize=(12, 8))  # Ajuste o tamanho da figura
    plt.barh(atividades_principais, frequencias, color='skyblue', height=0.5)  # Ajuste o espaçamento entre as barras
    plt.xlabel('Frequência')
    plt.ylabel('Atividades')
    plt.title('Principais Atividades do Processo')
    plt.gca().invert_yaxis()
    #plt.tight_layout()  # Ajuste o layout para evitar cortes de texto
    plt.show()

def plotar_dfg(data):
    # Verifica o nome das colunas presentes no dataframe
    print(data.columns)

    # Transforma os dados no formato CSV para o formato XES
    log = pm4py.format_dataframe(data, case_id='caseid', activity_key='activity', timestamp_key='time:timestamp')

    # Calcula o grafo de fluxo direcionado (DFG)
    dfg = dfg_algorithm.apply(log)

    # Plota o DFG
    gviz = dfg_visualizer.apply(dfg)
    dfg_visualizer.view(gviz)


# Carrega os dados do arquivo CSV
dados = pd.read_csv('dados.csv', sep=';')

# Executa o alinhamento heurístico para descoberta de processos
processos = alinhamento_heuristico(dados)

# Plota o gráfico com as principais atividades relacionadas ao processo
plotar_grafico(processos)

# Renomear a coluna 'timestamp' para 'time:timestamp'
dados.rename(columns={'timestamp': 'time:timestamp'}, inplace=True)

# Selecionar apenas as colunas relevantes para a análise do DFG
dados = dados[['caseid', 'activity']]

# Chamar a função para plotar o DFG
plotar_dfg(dados)

