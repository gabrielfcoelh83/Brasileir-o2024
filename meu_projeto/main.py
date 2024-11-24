import numpy as np
import pandas as pd
from datetime import datetime
import requests  # Certifique-se de importar a biblioteca requests
from bs4 import BeautifulSoup
from simulacao.simulacao import simulate_complete_season
from simulacao.classificacao import calculate_final_standings
from visualizacao.graficos import plot_final_classification, plot_relegation_probabilities

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

# Número de simulações
num_simulations = 10000

# Simula toda a temporada
final_positions = simulate_complete_season(df_tabela, num_simulations)

# Calcula a classificação final (média das posições)
avg_positions = calculate_final_standings(final_positions)

# Adiciona a coluna de classificação
df_tabela['Classificação Final'] = np.argsort(final_positions.mean(axis=0))

# Geração dos gráficos
plot_final_classification(df_tabela)
plot_relegation_probabilities(df_tabela)

# Exibe a tabela com a classificação final
df_tabela_sorted = df_tabela.sort_values('Classificação Final')
print(df_tabela_sorted)
