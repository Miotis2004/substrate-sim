import matplotlib.pyplot as plt
import numpy as np
import os
import json

def set_style():
    """Sets a style suitable for publication."""
    plt.rcParams.update({
        'font.size': 12,
        'axes.labelsize': 14,
        'axes.titlesize': 16,
        'xtick.labelsize': 12,
        'ytick.labelsize': 12,
        'legend.fontsize': 12,
        'lines.linewidth': 2,
        'figure.dpi': 300,
        'savefig.bbox': 'tight'
    })

def plot_time_series(time, rho_s, lam_series, events, title, filename):
    set_style()
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

    ax1.plot(time, rho_s, color='blue')
    ax1.set_ylabel(r'$\rho_s$ (Energy Density)')
    ax1.set_title(title)
    ax1.grid(True, alpha=0.3)

    ax2.plot(time, lam_series, color='red')
    ax2.set_ylabel(r'$\lambda$ (Nucleation Rate)')
    ax2.grid(True, alpha=0.3)

    # Raster plot for events
    event_times = time[events > 0]
    ax3.vlines(event_times, 0, 1, color='black', alpha=0.5)
    ax3.set_ylabel('Events')
    ax3.set_xlabel(r'$\tau$ (Time)')
    ax3.set_yticks([])

    plt.tight_layout()
    os.makedirs('figures', exist_ok=True)
    plt.savefig(os.path.join('figures', filename))
    plt.close()

def plot_spatial_snapshot(rho_grid, event_grid, time_val, filename):
    set_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    im1 = ax1.imshow(rho_grid, cmap='viridis', origin='lower')
    ax1.set_title(f'Substrate Density $\\rho_s$ at $\\tau = {time_val:.1f}$')
    plt.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)

    im2 = ax2.imshow(event_grid, cmap='Greys', origin='lower')
    ax2.set_title(f'Nucleation Events at $\\tau = {time_val:.1f}$')

    plt.tight_layout()
    os.makedirs('figures', exist_ok=True)
    plt.savefig(os.path.join('figures', filename))
    plt.close()

def plot_histograms(intervals, filename):
    set_style()
    plt.figure(figsize=(8, 5))
    plt.hist(intervals, bins=30, color='skyblue', edgecolor='black')
    plt.xlabel('Inter-event Interval')
    plt.ylabel('Frequency')
    plt.title('Distribution of Nucleation Intervals')

    os.makedirs('figures', exist_ok=True)
    plt.savefig(os.path.join('figures', filename))
    plt.close()

def generate_all_plots():
    data_dir = 'data'
    if not os.path.exists(data_dir):
        print("No data directory found. Run simulations first.")
        return

    for filename in os.listdir(data_dir):
        if not filename.endswith('.json'):
            continue

        filepath = os.path.join(data_dir, filename)
        with open(filepath, 'r') as f:
            data = json.load(f)

        base_name = filename.replace('.json', '')

        if 'single_cell' in filename or 'low_eta' in filename or 'high_k' in filename:
            # Reconstruct boolean events array
            T_max = data['T_max']
            dt = data['dt']
            num_steps = int(T_max / dt)
            time = np.linspace(0, T_max, num_steps)

            events = np.zeros(num_steps, dtype=int)
            event_times = np.array(data['event_times'])

            # Map event times back to indices roughly
            indices = np.searchsorted(time, event_times)
            indices = indices[indices < num_steps]
            events[indices] = 1

            plot_time_series(time, data['rho_s_time_series'], data['lambda_time_series'], events,
                             f'Time Series: {base_name}', f'{base_name}_timeseries.png')

            from src.metrics import compute_inter_event_intervals
            intervals = compute_inter_event_intervals(event_times)
            if len(intervals) > 0:
                plot_histograms(intervals, f'{base_name}_histogram.png')

        elif 'spatial' in filename:
            snapshots = data['snapshots']
            if len(snapshots) > 0:
                # Plot the final snapshot
                last_snap = snapshots[-1]
                plot_spatial_snapshot(np.array(last_snap['rho_grid']),
                                      np.array(last_snap['event_grid']),
                                      last_snap['time'],
                                      f'{base_name}_snapshot_final.png')

if __name__ == "__main__":
    generate_all_plots()
