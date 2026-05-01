import os
import json
import numpy as np

from src.substrate_model import simulate_single_cell

def run_low_eta_test(seed=42):
    print("Running Low Eta (High Depletion) Test...")

    # We set C to a more negative value to simulate low efficiency / high depletion
    params = {
        'rho_c': 5.0,
        'lambda_max': 1.0,
        'k': 2.0,
        'rho_eq': 4.5,
        'Gamma': 0.25,
        'R_0': 0.2,
        'C': -5.0  # Much lower C
    }

    dt = 0.01
    T_max = 100.0
    initial_rho_s = 6.0 # Start high

    results = simulate_single_cell(params, dt, T_max, initial_rho_s, seed=seed)

    output_data = {
        "parameters": params,
        "dt": dt,
        "T_max": T_max,
        "initial_rho_s": initial_rho_s,
        "seed": seed,
        "rho_s_time_series": results['rho_s'].tolist(),
        "lambda_time_series": results['lambda'].tolist(),
        "event_times": results['time'][results['events'] == 1].tolist()
    }

    os.makedirs('data', exist_ok=True)
    output_file = f"data/run_low_eta_{seed}.json"
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    run_low_eta_test()
