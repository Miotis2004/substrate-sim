import os
import json
import numpy as np

from src.substrate_model import simulate_single_cell

def run_high_k_burst_test(seed=42):
    print("Running High k (Burst) Test...")

    # We set a large k, which makes the nucleation rate highly sensitive to density, creating bursts
    # We also use a positive C (if we want runaway/oscillation) or a small negative C for sharp transitions.
    # To get oscillations/bursts without immediate collapse, C > 0 is often needed, but we can also
    # play with strong R_0 and negative C. Let's try high k with slight positive feedback or delayed damping.
    # We will use the toy model but set k very high.
    params = {
        'rho_c': 5.0,
        'lambda_max': 5.0,
        'k': 50.0,      # Extremely sensitive
        'rho_eq': 4.5,
        'Gamma': 0.1,   # weaker damping
        'R_0': 0.5,
        'C': -2.0       # Depletes energy quickly once threshold is hit
    }

    dt = 0.001       # Need smaller dt for high k stability
    T_max = 100.0
    initial_rho_s = 4.0 # Start below threshold

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
    output_file = f"data/run_high_k_burst_{seed}.json"
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    run_high_k_burst_test()
