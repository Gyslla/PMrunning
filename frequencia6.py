import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

def selecionar_arquivo():
    """
    Função para abrir uma janela do Windows e selecionar um arquivo CSV.

    Retorna:
        O caminho completo do arquivo selecionado.
    """
    root = Tk()
    root.withdraw()  # Oculta a janela principal

    caminho_arquivo = filedialog.askopenfilename(title="Selecione o arquivo CSV", filetypes=(("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")))
    return caminho_arquivo

def alinhamento_heuristico(data):
    """
    Função para calcular a frequência nominal e percentual das atividades.

    Parâmetros:
        - data: DataFrame contendo os dados do log de eventos.

    Retorna:
        Um dicionário contendo as atividades como chaves e uma tupla com a frequência nominal e percentual como valores.
    """
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
    """
    Função para plotar o gráfico de barras com a frequência nominal e percentual das atividades.

    Parâmetros:
        - frequencia_atividades: Dicionário contendo as atividades como chaves e uma tupla com a frequência nominal e percentual como valores.
    """
    # Ordenar as atividades por frequência decrescente
    frequencia_atividades = dict(sorted(frequencia_atividades.items(), key=lambda item: item[1][0], reverse=True))

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

    # Ajusta o título do gráfico para uma posição mais baixa
    plt.title('Frequência Nominal e Percentual das Atividades', pad=20)

    # Adiciona a escala para atividades adicionais
    if len(atividades) > 5:
        escala = {i: atividades[i] for i in range(len(atividades))}
        ax1.set_xticks(range(len(atividades)))
        ax1.set_xticklabels([str(i) for i in range(1, len(atividades) + 1)])
        ax1.tick_params(axis='x', direction='out', length=5, width=2)
        ax1.set_xlabel('Atividades')
        ax2.set_xlabel('Atividades')

        # Adiciona a legenda da escala ao lado direito do gráfico
        legenda_escala = '\n'.join([f"{i}: {atividade}" for i, atividade in escala.items()])
        plt.text(1.1, 0.5, f'Escala:\n{legenda_escala}', transform=ax1.transAxes, fontsize=8, verticalalignment='center', horizontalalignment='left')

    # Adiciona a logomarca como marca d'água
    img = plt.imread('Logo-Instituto-de-Computacao-1.png')
    imagebox = OffsetImage(img, zoom=0.3, alpha=0.1)
    ab = AnnotationBbox(imagebox, (0.5, 0.5), xycoords='axes fraction', frameon=False)
    ax1.add_artist(ab)

    plt.tight_layout()

    plt.show()

if __name__ == "__main__":
    # Solicitar ao usuário para selecionar o arquivo CSV
    caminho_arquivo = selecionar_arquivo()

    if caminho_arquivo:
        try:
            # Carregar os dados do arquivo CSV
            dados_csv = pd.read_csv(caminho_arquivo, sep=';', parse_dates=['timestamp'], dayfirst=True, encoding='latin1')

            # Executar o alinhamento heurístico para descoberta de processos
            frequencia_atividades = alinhamento_heuristico(dados_csv)

            # Plota o gráfico com as frequências nominal e percentual das atividades
            plotar_grafico(frequencia_atividades)

        except FileNotFoundError:
            print("Arquivo não encontrado. Verifique o caminho e tente novamente.")
