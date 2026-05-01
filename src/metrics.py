import numpy as np

def compute_inter_event_intervals(event_times):
    """
    Computes the intervals between consecutive events.
    """
    if len(event_times) < 2:
        return []
    return np.diff(event_times)

def compute_burstiness_index(intervals):
    """
    Computes the burstiness index of an event sequence.
    B = (sigma - mu) / (sigma + mu)
    where mu is the mean and sigma is the standard deviation of intervals.
    B = -1 for regular (periodic) events
    B = 0 for Poisson events
    B > 0 for bursty events
    """
    if len(intervals) < 2:
        return np.nan
    mu = np.mean(intervals)
    sigma = np.std(intervals)
    if mu + sigma == 0:
        return 0.0
    return (sigma - mu) / (sigma + mu)

def nearest_neighbor_distances(event_map):
    """
    Computes the nearest neighbor distance for each event in a binary 2D grid.
    event_map: 2D boolean or integer numpy array.
    """
    from scipy.spatial import KDTree

    # Get coordinates of events
    y, x = np.where(event_map > 0)
    if len(x) < 2:
        return []

    points = np.column_stack((x, y))
    tree = KDTree(points)

    # query(k=2) returns the distance to the point itself (dist=0) and the nearest neighbor
    distances, _ = tree.query(points, k=2)

    # Return the distance to the nearest neighbor (index 1)
    return distances[:, 1]

def spatial_variance(rho_grid):
    """
    Computes the spatial variance of the density field.
    """
    return np.var(rho_grid)
