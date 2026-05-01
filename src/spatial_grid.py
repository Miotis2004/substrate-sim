import numpy as np
from src.nucleation import lambda_rate
from src.substrate_model import intrinsic_generation, nucleation_feedback_term, damping_term

def simulate_spatial(params, dt, T_max, grid_size=(50, 50), initial_rho_mean=4.0, initial_rho_std=0.1, diffusion_coeff=0.1, depletion_magnitude=0.5, seed=None):
    """
    Simulate a 2D spatial grid.
    Returns the time series of the mean properties, event counts, and grid snapshots.
    """
    rng = np.random.default_rng(seed)

    num_steps = int(T_max / dt)
    time = np.linspace(0, T_max, num_steps)

    # Initialize grid
    rho_grid = rng.normal(loc=initial_rho_mean, scale=initial_rho_std, size=grid_size)

    # Data to return
    mean_rho_s = np.zeros(num_steps)
    mean_lambda = np.zeros(num_steps)
    total_events = np.zeros(num_steps, dtype=int)
    snapshots = [] # We'll save a few snapshots to avoid massive memory usage

    snapshot_interval = max(1, num_steps // 10) # Save ~10 snapshots

    # Helper to compute diffusion with periodic boundary conditions
    def compute_diffusion(grid):
        diff = np.zeros_like(grid)
        # Roll shifts the array: roll(grid, 1, axis=0) shifts down
        diff += np.roll(grid, 1, axis=0) + np.roll(grid, -1, axis=0)
        diff += np.roll(grid, 1, axis=1) + np.roll(grid, -1, axis=1)
        diff -= 4 * grid
        return diff

    for i in range(num_steps):
        # 1. Evaluate rates and derivatives for the current state
        R = intrinsic_generation(rho_grid, params)
        lam_grid = lambda_rate(rho_grid, params['lambda_max'], params['rho_c'], params['k'])

        # Feedback is evaluated dynamically. We use the analytical form for the derivative
        # C * lambda, but we ALSO implement local discrete event depletion separately.
        # To avoid double counting, we assume the C * lambda is the continuous background
        # expectation, but if we do discrete depletion, we shouldn't use C for the continuous part.
        # Actually, if we do explicit discrete events with discrete energy extraction, we should set C=0
        # in the continuous equation and handle it in the event step.
        # For simplicity, we stick to the continuous equation but add discrete localized depletion.

        damping = damping_term(rho_grid, params)
        diffusion = diffusion_coeff * compute_diffusion(rho_grid)

        drho = R + params['C'] * lam_grid + damping + diffusion

        # Euler step for PDE
        rho_grid = rho_grid + dt * drho

        # 2. Sample discrete events
        prob_grid = 1.0 - np.exp(-lam_grid * dt)
        event_grid = rng.random(grid_size) < prob_grid

        events_this_step = np.sum(event_grid)

        # 3. Apply local event depletion (if any)
        if events_this_step > 0:
            # For each event, reduce the local rho_s by depletion_magnitude
            rho_grid[event_grid] -= depletion_magnitude

        # Record metrics
        mean_rho_s[i] = np.mean(rho_grid)
        mean_lambda[i] = np.mean(lam_grid)
        total_events[i] = events_this_step

        if i % snapshot_interval == 0 or i == num_steps - 1:
            snapshots.append({
                'time': time[i],
                'rho_grid': rho_grid.copy(),
                'event_grid': event_grid.copy()
            })

    return {
        'time': time,
        'mean_rho_s': mean_rho_s,
        'mean_lambda': mean_lambda,
        'total_events': total_events,
        'snapshots': snapshots
    }
