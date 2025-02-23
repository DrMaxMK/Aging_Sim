import pandas as pd
import config

def run_simulation(stage, years=config.YEARS):
    """Runs the simulation for a given number of years."""
    for year in range(years):
        stage.step(year)

def save_results(stage, filename="simulation_results.csv"):
    """Converts simulation stats to a DataFrame and saves as CSV."""
    df = pd.DataFrame(stage.get_stats())
    df.to_csv(filename, index=False)
    #print(f"Simulation results saved as '{filename}'.")
    return df

def extract_death_ages(stage):
    """Extracts all death ages from the simulation stats."""
    return [age for year_data in stage.stats for age in year_data["death_ages"]]
