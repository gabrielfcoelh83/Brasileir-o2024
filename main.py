# Instala todas as dependências para testar no Google Colab


import numpy as np
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import imgkit
from datetime import datetime
import pytz
from IPython.display import display, Image as IPImage

# URL da página da tabela do Campeonato Brasileiro 2024
url = "https://www.api-futebol.com.br/campeonato/campeonato-brasileiro/2024"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extrai e converte dados da tabela diretamente para DataFrame
tabela = [[col.get_text(strip=True) for col in row.find_all(["td", "th"])] for row in soup.select("table tr")]
df_tabela = pd.DataFrame(tabela[1:], columns=tabela[0]).drop(columns=["Recentes"])

# Renomeia colunas e ajusta tipos de dados
df_tabela = df_tabela.rename(columns={"%": "Aproveitamento (%)", "Probabilidade de Rebaixamento (%)": "Probabilidade de Rebaixamento\n(%)"})
df_tabela['PTS'] = pd.to_numeric(df_tabela['PTS'], errors='coerce')
df_tabela['J'] = pd.to_numeric(df_tabela['J'], errors='coerce')
df_tabela['Jogos Restantes'] = 38 - df_tabela['J']

# Configurações e funções de simulação
teams, relegation_spots, num_simulations = df_tabela.shape[0], 4, 10000

def generate_random_remaining_matches(df):
    jogos_restantes, jogos_faltantes = [], df['Jogos Restantes'].copy().values
    while np.sum(jogos_faltantes) > 0:
        times_pendentes = np.where(jogos_faltantes > 0)[0]
        if len(times_pendentes) < 2:
            break
        team1, team2 = np.random.choice(times_pendentes, 2, replace=False)
        jogos_restantes.append((team1, team2))
        jogos_faltantes[team1] -= 1
        jogos_faltantes[team2] -= 1
    return jogos_restantes

def simulate_matches(current_points, jogos_restantes):
    team_points = current_points.copy()
    for team1, team2 in jogos_restantes:
        outcome = np.random.choice([0, 1, 3])
        if outcome == 3:
            team_points[team1] += 3
        elif outcome == 1:
            team_points[team1] += 1
            team_points[team2] += 1
        else:
            team_points[team2] += 3
    return team_points

def calculate_relegation_probabilities(df, num_simulations):
    relegation_probabilities = np.zeros(teams)
    current_points = df['PTS'].values
    for _ in tqdm(range(num_simulations), desc="Simulando Campeonatos"):
        jogos_restantes = generate_random_remaining_matches(df)
        final_points = simulate_matches(current_points, jogos_restantes)
        relegated_indices = np.argsort(final_points)[::-1][-relegation_spots:]
        relegation_probabilities[relegated_indices] += 1
    return (relegation_probabilities / num_simulations) * 100

# Calcula probabilidades e exibe resultado
df_tabela['Probabilidade de Rebaixamento\n(%)'] = calculate_relegation_probabilities(df_tabela, num_simulations).round(2)
timestamp = datetime.now(pytz.timezone("America/Sao_Paulo")).strftime("%d/%m/%Y %H:%M")

# Filtra e ordena por probabilidade de rebaixamento para o gráfico
df_grafico = df_tabela[df_tabela['Probabilidade de Rebaixamento\n(%)'] > 0].sort_values('Probabilidade de Rebaixamento\n(%)', ascending=False)

# Define cores para as barras: os 4 maiores em tons de vermelho, os demais em azul
colors = ['red' if i < 4 else 'blue' for i in range(len(df_grafico))]
red_shades = [(1, 1 - prob / 100, 1 - prob / 100) if i < 4 else 'blue' for i, prob in enumerate(df_grafico['Probabilidade de Rebaixamento\n(%)'])]

# Criação do gráfico
plt.figure(figsize=(12, 6))
bars = plt.bar(df_grafico['Time'], df_grafico['Probabilidade de Rebaixamento\n(%)'], color=red_shades)
plt.xlabel('Time')
plt.ylabel('Probabilidade de Rebaixamento (%)')
plt.title(f'Probabilidade de Rebaixamento de Cada Time\nAtualizado em: {timestamp}')
plt.xticks(rotation=45, ha='right')

# Adiciona os rótulos de porcentagem em cada barra
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.2f}%', ha='center', va='bottom')

plt.tight_layout()
plt.savefig('grafico_probabilidade_rebaixamento.png')
plt.show()

# Estiliza e exibe tabela como imagem
styled_table = df_tabela.style.set_caption(f'Tabela Atualizada em: {timestamp}').set_table_styles([
    {'selector': 'thead th', 'props': [('background-color', '#4CAF50'), ('color', 'white'), ('font-weight', 'bold')]},
    {'selector': 'tbody td', 'props': [('border', '1px solid #ddd'), ('padding', '8px'), ('text-align', 'center')]},
    {'selector': 'tbody tr:nth-child(even)', 'props': [('background-color', '#f2f2f2')]},
    {'selector': 'tbody tr:hover', 'props': [('background-color', '#ddd')]}
]).set_properties(**{'font-family': 'Arial', 'font-size': '12px'}).format({'Probabilidade de Rebaixamento\n(%)': "{:.2f}"})

html_table = styled_table.to_html()
imgkit.from_string(html_table, 'tabela_probabilidade_rebaixamento.png')
display(IPImage(filename='tabela_probabilidade_rebaixamento.png'))