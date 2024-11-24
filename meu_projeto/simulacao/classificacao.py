import numpy as np

def calculate_final_standings(final_positions):
    # Ordena os times pela média de pontos e retorna a classificação final
    avg_positions = np.argsort(final_positions.mean(axis=0))  # Ordena os times pela média de pontos
    return avg_positions
