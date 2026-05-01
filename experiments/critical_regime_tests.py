import json
import os
import numpy as np

from src.nucleation import lambda_rate
from src.substrate_model import rk4_step
from src.metrics import compute_temporal_metrics, compute_inter_event_intervals
from src.plotting import plot_time_series, plot_histogram, plot_critical_regime_comparison


DATA_DIR = 'data'
FIG_DIR = 'figures'


def run_single_case(name, params, steps, dt, seed, rho_initial, sigma=0.0):
    rng = np.random.default_rng(seed)
    time = np.arange(steps) * dt
    rho_s = np.zeros(steps)
    lam = np.zeros(steps)
    events = np.zeros(steps, dtype=int)
    rho_s[0] = rho_initial
    lam[0] = lambda_rate(rho_s[0], params['lambda_max'], params['rho_c'], params['k'])

    for i in range(1, steps):
        rho_s[i] = rk4_step(rho_s[i - 1], params, dt)
        if sigma > 0:
            rho_s[i] += rng.normal(0.0, sigma)
        lam[i] = lambda_rate(rho_s[i], params['lambda_max'], params['rho_c'], params['k'])
        p = 1.0 - np.exp(-lam[i] * dt)
        events[i] = int(rng.random() < p)

    event_times = time[events > 0]
    metrics = compute_temporal_metrics(time, rho_s, lam, events, params['rho_c'])

    payload = {
        'run_name': name,
        'parameters': params,
        'steps': steps,
        'dt': dt,
        'seed': seed,
        'sigma': sigma,
        'rho_s_time_series': rho_s.tolist(),
        'lambda_time_series': lam.tolist(),
        'event_times': event_times.tolist(),
        'metrics': metrics,
    }
    return payload


def run_poisson_baseline(lambda_constant, steps, dt, seed):
    rng = np.random.default_rng(seed)
    time = np.arange(steps) * dt
    lam = np.full(steps, lambda_constant)
    events = (rng.random(steps) < (1.0 - np.exp(-lambda_constant * dt))).astype(int)
    event_times = time[events > 0]
    intervals = compute_inter_event_intervals(event_times)
    payload = {
        'run_name': 'poisson_baseline',
        'parameters': {'lambda_constant': float(lambda_constant)},
        'steps': steps,
        'dt': dt,
        'seed': seed,
        'event_times': event_times.tolist(),
        'metrics': {
            'event_count': int(events.sum()),
            'mean_inter_event_interval': float(np.mean(intervals)) if len(intervals) else np.nan,
            'var_inter_event_interval': float(np.var(intervals)) if len(intervals) else np.nan,
            'burstiness_index': float((np.std(intervals)-np.mean(intervals))/(np.std(intervals)+np.mean(intervals))) if len(intervals) > 1 else np.nan,
        }
    }
    return payload, intervals


def save_json(data, filename):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(os.path.join(DATA_DIR, filename), 'w') as f:
        json.dump(data, f, indent=2)


def main():
    os.makedirs(FIG_DIR, exist_ok=True)
    steps, dt, seed = 5000, 0.05, 42

    cases = [
        ('critical_hover', {'rho_c': 5.0, 'rho_eq': 5.0, 'Gamma': 0.05, 'k': 10.0, 'lambda_max': 1.0, 'R_0': 0.05, 'C': -0.05}, 4.9, 0.0),
        ('low_damping', {'rho_c': 5.0, 'rho_eq': 5.0, 'Gamma': 0.01, 'k': 8.0, 'lambda_max': 1.0, 'R_0': 0.03, 'C': -0.03}, 4.95, 0.0),
        ('noise_threshold', {'rho_c': 5.0, 'rho_eq': 5.0, 'Gamma': 0.05, 'k': 12.0, 'lambda_max': 1.0, 'R_0': 0.04, 'C': -0.04}, 4.95, 0.03),
        ('avalanche_high_k', {'rho_c': 5.0, 'rho_eq': 5.0, 'Gamma': 0.03, 'k': 25.0, 'lambda_max': 1.0, 'R_0': 0.035, 'C': -0.035}, 4.98, 0.02),
    ]

    outputs = []
    for name, params, rho_initial, sigma in cases:
        out = run_single_case(name, params, steps, dt, seed, rho_initial, sigma)
        save_json(out, f'run_{name}_42.json')
        intervals = np.array(out['metrics']['inter_event_intervals'])
        plot_time_series(np.arange(steps)*dt, np.array(out['rho_s_time_series']), np.array(out['lambda_time_series']), np.array(out['event_times']), f'{name.replace("_", " ").title()} Regime', f'run_{name}_42_timeseries.png')
        if len(intervals):
            plot_histogram(intervals, f'Inter-event intervals: {name}', f'run_{name}_42_histogram.png')
        outputs.append(out)

    lambda_constant = outputs[0]['metrics']['mean_lambda']
    base, base_intervals = run_poisson_baseline(lambda_constant, steps, dt, seed)
    save_json(base, 'run_poisson_baseline_42.json')
    if len(base_intervals):
        plot_histogram(base_intervals, 'Inter-event intervals: Poisson baseline', 'run_poisson_baseline_42_histogram.png')

    for out in outputs:
        out['metrics']['poisson_comparison_score'] = float((out['metrics']['var_inter_event_interval'] - np.var(base_intervals)) / np.var(base_intervals)) if len(base_intervals) > 1 else np.nan
        save_json(out, f'run_{out["run_name"]}_42.json')

    summary = [{'name': o['run_name'], **o['metrics']} for o in outputs]
    summary.append({'name': 'poisson_baseline', **base['metrics']})
    plot_critical_regime_comparison(summary, 'critical_regime_comparison.png')


if __name__ == '__main__':
    main()
