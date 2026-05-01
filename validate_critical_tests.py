import glob
import json
import numpy as np


def classify(metrics, rho_c):
    b = metrics.get('burstiness_index', np.nan)
    tv = metrics.get('tail_variance', np.nan)
    frac = metrics.get('fraction_above_threshold', 0.0)
    final_rho = metrics.get('final_rho_s', np.nan)
    mean_lam = metrics.get('mean_lambda', np.nan)
    max_lam = metrics.get('max_lambda', np.nan)

    if np.isfinite(final_rho) and final_rho < rho_c and np.isfinite(mean_lam) and mean_lam < 0.05:
        status = 'depleted'
    elif np.isfinite(frac) and frac > 0.9 and np.isfinite(max_lam) and max_lam > 0.95:
        status = 'runaway'
    elif np.isfinite(b) and b > 0.2:
        status = 'bursty'
    elif np.isfinite(b) and b < -0.2:
        status = 'regularized'
    elif np.isfinite(tv) and tv < 1e-3 and (not np.isfinite(b) or abs(b) < 0.1):
        status = 'stable'
    else:
        status = 'stable'
    return status


def main():
    files = sorted(glob.glob('data/run_*_42.json'))
    for fp in files:
        if 'spatial' in fp:
            continue
        with open(fp) as f:
            d = json.load(f)
        run = d.get('run_name', fp)
        metrics = d.get('metrics', {})
        rho_c = d.get('parameters', {}).get('rho_c', 5.0)
        status = classify(metrics, rho_c)
        print(f'Run: {run}')
        print(f'Status: {status}')
        print(f"Burstiness Index: {metrics.get('burstiness_index', np.nan)}")
        print(f"Tail Variance: {metrics.get('tail_variance', np.nan)}")
        print(f"Fraction Above Threshold: {metrics.get('fraction_above_threshold', np.nan)}")
        print(f"Event Count: {metrics.get('event_count', np.nan)}")
        print('Interpretation: classification based on burstiness, tail stability, and threshold occupancy.')
        print('-' * 60)


if __name__ == '__main__':
    main()
