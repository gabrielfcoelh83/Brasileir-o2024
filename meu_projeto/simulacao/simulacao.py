import numpy as np
from tqdm import tqdm

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

def simulate_complete_season(df, num_simulations):
    final_positions = np.zeros((num_simulations, len(df)))  # Armazena a posição final de cada time em cada simulação
    current_points = df['PTS'].values  # Pontuação atual dos times

    for sim in tqdm(range(num_simulations), desc="Simulando Temporada Completa"):
        jogos_restantes = generate_random_remaining_matches(df)
        final_points = simulate_matches(current_points, jogos_restantes)  # Simula os jogos restantes
        final_positions[sim] = final_points  # Armazena os pontos finais para cada simulação

    return final_positions
