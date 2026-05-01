import json
import os
import numpy as np
import matplotlib.pyplot as plt

from src.nucleation import lambda_rate
from src.metrics import nearest_neighbor_distances, spatial_variance, pair_correlation_approx


def laplacian_periodic(grid):
    return (np.roll(grid, 1, 0) + np.roll(grid, -1, 0) + np.roll(grid, 1, 1) + np.roll(grid, -1, 1) - 4 * grid)


def apply_radial_depletion(rho, x, y, radius, strength):
    n = rho.shape[0]
    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            dist2 = dx * dx + dy * dy
            if dist2 <= radius * radius:
                xx = (x + dx) % n
                yy = (y + dy) % n
                depletion = strength * np.exp(-dist2 / (2 * radius * radius))
                rho[xx, yy] -= depletion


def main():
    params = {
        'grid_size': 75, 'steps': 1000, 'dt': 0.1, 'seed': 42,
        'rho_c': 5.0, 'rho_eq': 5.0, 'k': 10.0, 'lambda_max': 1.0,
        'R_0': 0.03, 'C': -0.02, 'Gamma': 0.02,
        'depletion_radius': 4, 'depletion_strength': 0.25,
        'recovery_rate': 0.02, 'diffusion_rate': 0.01,
    }
    rng = np.random.default_rng(params['seed'])
    n = params['grid_size']
    rho = np.full((n, n), 4.95)
    event_density = np.zeros((n, n), dtype=int)
    event_points, event_times = [], []

    for step in range(params['steps']):
        t = step * params['dt']
        lam = lambda_rate(rho, params['lambda_max'], params['rho_c'], params['k'])
        probs = 1.0 - np.exp(-lam * params['dt'])
        events = rng.random((n, n)) < probs

        xs, ys = np.where(events)
        for x, y in zip(xs, ys):
            event_points.append([int(x), int(y)])
            event_times.append(float(t))
            event_density[x, y] += 1
            apply_radial_depletion(rho, x, y, params['depletion_radius'], params['depletion_strength'])

        rho += params['recovery_rate'] * (params['rho_eq'] - rho) * params['dt']
        rho += params['diffusion_rate'] * laplacian_periodic(rho) * params['dt']
        rho += (params['R_0'] + params['C'] * lam - params['Gamma'] * (rho - params['rho_eq'])) * params['dt']

    nnd = nearest_neighbor_distances(event_points)
    random_pts = rng.integers(0, n, size=(len(event_points), 2)) if len(event_points) else np.empty((0, 2))
    random_nnd = nearest_neighbor_distances(random_pts)

    payload = {
        'run_name': 'spatial_feedback',
        'parameters': params,
        'event_points': event_points,
        'event_times': event_times,
        'final_density_grid': rho.tolist(),
        'event_density_map': event_density.tolist(),
        'nearest_neighbor_distances': np.asarray(nnd).tolist(),
        'mean_nearest_neighbor_distance': float(np.mean(nnd)) if len(nnd) else np.nan,
        'spatial_variance_event_density': spatial_variance(event_density),
        'pair_correlation': pair_correlation_approx(event_points, n),
        'poisson_nearest_neighbor_mean': float(np.mean(random_nnd)) if len(random_nnd) else np.nan,
        'spatial_clustering_score': float(np.mean(nnd) - np.mean(random_nnd)) if len(nnd) and len(random_nnd) else np.nan,
    }

    os.makedirs('data', exist_ok=True)
    os.makedirs('figures', exist_ok=True)
    with open('data/run_spatial_feedback_42.json', 'w') as f:
        json.dump(payload, f, indent=2)

    plt.figure(figsize=(6, 5))
    plt.imshow(rho, origin='lower', cmap='viridis')
    plt.colorbar(label=r'Final $\rho_s$')
    plt.title('Final substrate density field')
    plt.savefig('figures/run_spatial_feedback_42_density_final.png', bbox_inches='tight', dpi=200)
    plt.close()

    plt.figure(figsize=(6, 6))
    if len(event_points):
        pts = np.asarray(event_points)
        plt.scatter(pts[:, 1], pts[:, 0], s=2, alpha=0.4)
    plt.title('Spatial event coordinates')
    plt.xlabel('y'); plt.ylabel('x')
    plt.savefig('figures/run_spatial_feedback_42_events.png', bbox_inches='tight', dpi=200)
    plt.close()

    plt.figure(figsize=(6, 4))
    if len(nnd):
        plt.hist(nnd, bins=25, alpha=0.8, label='Feedback')
    if len(random_nnd):
        plt.hist(random_nnd, bins=25, alpha=0.5, label='Poisson matched count')
    plt.legend()
    plt.xlabel('Nearest-neighbor distance')
    plt.ylabel('Count')
    plt.title('Nearest-neighbor distance comparison')
    plt.savefig('figures/run_spatial_feedback_42_nearest_neighbor_histogram.png', bbox_inches='tight', dpi=200)
    plt.close()


if __name__ == '__main__':
    main()
