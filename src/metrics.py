import numpy as np


def compute_inter_event_intervals(event_times):
    if len(event_times) < 2:
        return np.array([])
    return np.diff(np.asarray(event_times, dtype=float))


def compute_burstiness_index(intervals):
    intervals = np.asarray(intervals, dtype=float)
    if intervals.size < 2:
        return np.nan
    mu = np.mean(intervals)
    sigma = np.std(intervals)
    if mu + sigma == 0:
        return 0.0
    return float((sigma - mu) / (sigma + mu))


def compute_cluster_count(event_times, interval_threshold=1.0):
    intervals = compute_inter_event_intervals(event_times)
    if intervals.size == 0:
        return 0
    in_cluster = intervals < interval_threshold
    count = 0
    i = 0
    while i < len(in_cluster):
        if in_cluster[i]:
            count += 1
            while i < len(in_cluster) and in_cluster[i]:
                i += 1
        else:
            i += 1
    return int(count)


def compute_poisson_comparison_score(intervals, baseline_intervals):
    intervals = np.asarray(intervals, dtype=float)
    baseline_intervals = np.asarray(baseline_intervals, dtype=float)
    if intervals.size < 2 or baseline_intervals.size < 2:
        return np.nan
    obs_var = np.var(intervals)
    base_var = np.var(baseline_intervals)
    if base_var == 0:
        return np.nan
    return float((obs_var - base_var) / base_var)


def compute_temporal_metrics(time, rho_s, lam_series, events, rho_c, tail_fraction=0.2, cluster_interval_threshold=1.0, poisson_baseline_intervals=None):
    time = np.asarray(time)
    rho_s = np.asarray(rho_s)
    lam_series = np.asarray(lam_series)
    events = np.asarray(events)

    event_times = time[events > 0]
    intervals = compute_inter_event_intervals(event_times)

    tail_start = int((1 - tail_fraction) * len(rho_s))
    tail_var = float(np.var(rho_s[tail_start:])) if len(rho_s) else np.nan

    metrics = {
        "event_count": int(events.sum()),
        "mean_inter_event_interval": float(np.mean(intervals)) if intervals.size else np.nan,
        "var_inter_event_interval": float(np.var(intervals)) if intervals.size else np.nan,
        "burstiness_index": compute_burstiness_index(intervals),
        "tail_variance": tail_var,
        "mean_lambda": float(np.mean(lam_series)),
        "final_rho_s": float(rho_s[-1]),
        "max_lambda": float(np.max(lam_series)),
        "min_lambda": float(np.min(lam_series)),
        "fraction_above_threshold": float(np.mean(rho_s > rho_c)),
        "cluster_count": compute_cluster_count(event_times, cluster_interval_threshold),
        "poisson_comparison_score": compute_poisson_comparison_score(intervals, poisson_baseline_intervals) if poisson_baseline_intervals is not None else np.nan,
        "inter_event_intervals": intervals.tolist(),
    }
    return metrics


def nearest_neighbor_distances(event_points):
    points = np.asarray(event_points, dtype=float)
    if len(points) < 2:
        return np.array([])
    diffs = points[:, None, :] - points[None, :, :]
    dists = np.sqrt(np.sum(diffs ** 2, axis=2))
    np.fill_diagonal(dists, np.inf)
    return np.min(dists, axis=1)


def spatial_variance(event_density_map):
    return float(np.var(event_density_map))


def pair_correlation_approx(event_points, grid_size, max_radius=15, bins=15):
    points = np.asarray(event_points, dtype=float)
    if len(points) < 2:
        return {"r": [], "g_r": []}
    diffs = points[:, None, :] - points[None, :, :]
    dists = np.sqrt(np.sum(diffs ** 2, axis=2))
    dists = dists[np.triu_indices(len(points), k=1)]
    hist, edges = np.histogram(dists, bins=bins, range=(0, max_radius))
    r = 0.5 * (edges[:-1] + edges[1:])
    area = grid_size * grid_size
    density = len(points) / area
    annulus_areas = np.pi * (edges[1:] ** 2 - edges[:-1] ** 2)
    expected = annulus_areas * density * len(points) / 2
    g_r = np.divide(hist, expected, out=np.zeros_like(hist, dtype=float), where=expected > 0)
    return {"r": r.tolist(), "g_r": g_r.tolist()}
