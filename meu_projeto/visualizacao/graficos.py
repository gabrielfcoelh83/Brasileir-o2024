import matplotlib.pyplot as plt

def plot_final_classification(df):
    # Função para criar o gráfico de classificação final com base nas simulações
    plt.figure(figsize=(12, 6))
    plt.bar(df['Time'], df['Classificação Final'], color='skyblue')
    plt.xlabel('Time')
    plt.ylabel('Classificação Final')
    plt.title('Classificação Final Média do Campeonato Brasileiro 2024')
    plt.xticks(rotation=45, ha='right')

    # Adiciona os rótulos de cada time nas barras
    for i, v in enumerate(df['Classificação Final']):
        plt.text(i, v + 0.5, str(v), ha='center', va='bottom')

    plt.tight_layout()
    plt.show()

def plot_relegation_probabilities(df):
    # Função para plotar a probabilidade de rebaixamento
    df_relegation = df[df['Probabilidade de Rebaixamento\n(%)'] > 0]
    plt.figure(figsize=(12, 6))
    plt.bar(df_relegation['Time'], df_relegation['Probabilidade de Rebaixamento\n(%)'], color='red')
    plt.xlabel('Time')
    plt.ylabel('Probabilidade de Rebaixamento (%)')
    plt.title('Probabilidade de Rebaixamento dos Times no Campeonato Brasileiro 2024')
    plt.xticks(rotation=45, ha='right')

    # Adiciona as porcentagens nas barras
    for i, v in enumerate(df_relegation['Probabilidade de Rebaixamento\n(%)']):
        plt.text(i, v + 0.5, f'{v:.2f}%', ha='center', va='bottom')

    plt.tight_layout()
    plt.show()
