import numpy as np

def lambda_rate(rho_s, lambda_max, rho_c, k):
    """
    Sigmoid nucleation rate function.
    λ(ρₛ) = λ_max / [1 + exp(-k(ρₛ - ρ_c))]
    """
    return lambda_max / (1.0 + np.exp(-k * (rho_s - rho_c)))

def sample_events(rate, dt, rng=None):
    """
    Sample nucleation events for a given rate and timestep.
    Approximates as a Bernoulli process for small dt.
    """
    if rng is None:
        rng = np.random.default_rng()
    prob = 1.0 - np.exp(-rate * dt)
    return rng.random(np.shape(rate)) < prob
