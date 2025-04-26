import pandas as pd
import matplotlib.pyplot as plt

def alinhamento_heuristico(data):
    # Inicialização das estruturas de dados
    frequencia_atividades = {}

    # Calcular a frequência de cada atividade
    total_casos = len(data)
    for atividade in data['activity']:
        frequencia_atividades[atividade] = frequencia_atividades.get(atividade, 0) + 1

    # Calcular a frequência percentual de cada atividade
    for atividade, frequencia in frequencia_atividades.items():
        frequencia_atividades[atividade] = (frequencia, frequencia / total_casos * 100)

    return frequencia_atividades

def plotar_grafico(frequencia_atividades):
    atividades = list(frequencia_atividades.keys())
    frequencias_nominais = [item[0] for item in frequencia_atividades.values()]
    frequencias_percentuais = [item[1] for item in frequencia_atividades.values()]

    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Barra de frequência nominal
    ax1.bar(atividades, frequencias_nominais, color='skyblue')
    ax1.set_ylabel('Frequência Nominal')
    ax1.set_ylim(0, max(frequencias_nominais) * 1.1)  # Ajusta o limite do eixo y para evitar sobreposição com o segundo eixo

    # Eixo y da frequência percentual
    ax2 = ax1.twinx()
    ax2.plot(atividades, frequencias_percentuais, color='orange', marker='o')
    ax2.set_ylabel('Frequência Percentual (%)')
    ax2.set_ylim(0, 100)

    # Ajusta o texto do eixo x para até 20 caracteres
    plt.xticks(rotation=45, ha='right', fontsize=8)
    ax1.set_xticklabels([atividade[:20] + ' [...]' if len(atividade) > 20 else atividade for atividade in atividades])

    # Ajusta o título do gráfico para uma posição mais baixa
    plt.title('Frequência Nominal e Percentual das Atividades', pad=20)

    plt.tight_layout()

    plt.show()

# Carregar os dados do arquivo CSV
dados_csv = pd.read_csv('dados.csv', sep=';', parse_dates=['timestamp'], dayfirst=True, encoding='latin1')

# Executar o alinhamento heurístico para descoberta de processos
frequencia_atividades = alinhamento_heuristico(dados_csv)

# Plota o gráfico com as frequências nominal e percentual das atividades
plotar_grafico(frequencia_atividades)
