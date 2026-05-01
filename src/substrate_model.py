import numpy as np
from .nucleation import lambda_rate

def intrinsic_generation(rho_s, params):
    """R(ρₛ)"""
    return params.get('R_0', 0.2)

def nucleation_feedback_term(rho_s, params):
    """C * λ(ρₛ), where C = ηE_u - E_n"""
    C = params['C']
    rate = lambda_rate(rho_s, params['lambda_max'], params['rho_c'], params['k'])
    return C * rate

def damping_term(rho_s, params):
    """-Γ * (ρₛ - ρ_eq)"""
    return -params['Gamma'] * (rho_s - params['rho_eq'])

def drho_dt(rho_s, params):
    """Total derivative: dρₛ/dτ"""
    R = intrinsic_generation(rho_s, params)
    feedback = nucleation_feedback_term(rho_s, params)
    damping = damping_term(rho_s, params)
    return R + feedback + damping

def rk4_step(rho_s, params, dt):
    """4th order Runge-Kutta step."""
    k1 = drho_dt(rho_s, params)
    k2 = drho_dt(rho_s + 0.5 * dt * k1, params)
    k3 = drho_dt(rho_s + 0.5 * dt * k2, params)
    k4 = drho_dt(rho_s + dt * k3, params)
    return rho_s + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

def simulate_single_cell(params, dt, T_max, initial_rho_s, seed=None):
    """
    Simulate a single-cell model.
    Returns dictionaries of time series.
    """
    rng = np.random.default_rng(seed)

    num_steps = int(T_max / dt)
    time = np.linspace(0, T_max, num_steps)

    rho_s = np.zeros(num_steps)
    rho_s[0] = initial_rho_s

    lam_series = np.zeros(num_steps)
    lam_series[0] = lambda_rate(rho_s[0], params['lambda_max'], params['rho_c'], params['k'])

    events = np.zeros(num_steps, dtype=int)

    for i in range(1, num_steps):
        rho_s[i] = rk4_step(rho_s[i-1], params, dt)
        lam_series[i] = lambda_rate(rho_s[i], params['lambda_max'], params['rho_c'], params['k'])

        prob = 1.0 - np.exp(-lam_series[i] * dt)
        if rng.random() < prob:
            events[i] = 1

    return {
        'time': time,
        'rho_s': rho_s,
        'lambda': lam_series,
        'events': events
    }
