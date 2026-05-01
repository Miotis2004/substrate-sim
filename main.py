import argparse
import json
import os
import numpy as np

from src.substrate_model import simulate_single_cell

def run_single_cell(args):
    print("Running single-cell baseline...")
    # Default params from the toy model
    params = {
        'rho_c': 5.0,
        'lambda_max': 1.0,
        'k': 2.0,
        'rho_eq': 4.5,
        'Gamma': 0.25,
        'R_0': 0.2,
        'C': -1.0
    }

    dt = 0.01
    T_max = 100.0
    initial_rho_s = 4.0

    results = simulate_single_cell(params, dt, T_max, initial_rho_s, seed=args.seed)

    output_data = {
        "parameters": params,
        "dt": dt,
        "T_max": T_max,
        "initial_rho_s": initial_rho_s,
        "seed": args.seed,
        "rho_s_time_series": results['rho_s'].tolist(),
        "lambda_time_series": results['lambda'].tolist(),
        "event_times": results['time'][results['events'] == 1].tolist()
    }

    output_file = args.output or f"data/run_single_cell_{args.seed}.json"
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)
    print(f"Results saved to {output_file}")


def main():
    parser = argparse.ArgumentParser(description="SubstrateSim Runner")
    parser.add_argument('--mode', choices=['single-cell', 'spatial', 'experiment'], default='single-cell', help="Run mode")
    parser.add_argument('--experiment', type=str, help="Named experiment to run")
    parser.add_argument('--seed', type=int, default=42, help="Random seed for deterministic runs")
    parser.add_argument('--output', type=str, help="Override output file path")

    args = parser.parse_args()

    if args.mode == 'single-cell':
        run_single_cell(args)
    elif args.mode == 'spatial':
        from src.spatial_grid import simulate_spatial
        print("Running spatial simulation...")
        params = {
            'rho_c': 5.0,
            'lambda_max': 1.0,
            'k': 2.0,
            'rho_eq': 4.5,
            'Gamma': 0.25,
            'R_0': 0.2,
            'C': -1.0
        }
        dt = 0.01
        T_max = 100.0
        results = simulate_spatial(params, dt, T_max, seed=args.seed)

        # We need to make snapshots serializable
        snapshots_serializable = []
        for snap in results['snapshots']:
            snapshots_serializable.append({
                'time': snap['time'],
                'rho_grid': snap['rho_grid'].tolist(),
                'event_grid': snap['event_grid'].astype(int).tolist()
            })

        output_data = {
            "parameters": params,
            "dt": dt,
            "T_max": T_max,
            "seed": args.seed,
            "mean_rho_s": results['mean_rho_s'].tolist(),
            "mean_lambda": results['mean_lambda'].tolist(),
            "total_events": results['total_events'].tolist(),
            "snapshots": snapshots_serializable
        }

        output_file = args.output or f"data/run_spatial_{args.seed}.json"
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)
        print(f"Results saved to {output_file}")
    elif args.mode == 'experiment':
        if args.experiment == 'low_eta':
            from experiments.low_eta_test import run_low_eta_test
            run_low_eta_test(seed=args.seed)
        elif args.experiment == 'high_k':
            from experiments.high_k_burst_test import run_high_k_burst_test
            run_high_k_burst_test(seed=args.seed)
        else:
            print(f"Unknown experiment: {args.experiment}")

if __name__ == "__main__":
    main()
