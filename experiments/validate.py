import os
import json
import numpy as np
from src.metrics import compute_inter_event_intervals, compute_burstiness_index

def validate_baseline(filepath):
    print(f"Validating {filepath}...")
    with open(filepath, 'r') as f:
        data = json.load(f)

    event_times = data['event_times']
    intervals = compute_inter_event_intervals(event_times)
    burstiness = compute_burstiness_index(intervals)

    # Basic sanity checks
    rho_s = np.array(data['rho_s_time_series'])

    # Check if system reached a somewhat stable state (variance in last 10% is low)
    tail_len = int(len(rho_s) * 0.1)
    tail_var = np.var(rho_s[-tail_len:])

    print(f"  Burstiness Index: {burstiness:.4f} (Expected near 0 for Poisson-ish)")
    print(f"  Tail Variance (rho_s): {tail_var:.6f}")

    if tail_var < 0.1:
        print("  Status: STABLE")
    else:
        print("  Status: UNSTABLE/OSCILLATING")

def validate_all():
    data_dir = 'data'
    if not os.path.exists(data_dir):
        print("No data directory found. Run simulations first.")
        return

    for filename in os.listdir(data_dir):
        if filename.endswith('.json') and 'single_cell' in filename:
            validate_baseline(os.path.join(data_dir, filename))
        if filename.endswith('.json') and 'low_eta' in filename:
            validate_baseline(os.path.join(data_dir, filename))
        if filename.endswith('.json') and 'high_k' in filename:
            validate_baseline(os.path.join(data_dir, filename))

if __name__ == "__main__":
    validate_all()
