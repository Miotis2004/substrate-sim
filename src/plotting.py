import matplotlib.pyplot as plt
import numpy as np
import os


def set_style():
    plt.rcParams.update({
        'font.size': 12,
        'axes.labelsize': 12,
        'axes.titlesize': 14,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'lines.linewidth': 1.7,
        'figure.dpi': 200,
        'savefig.bbox': 'tight'
    })


def plot_time_series(time, rho_s, lam_series, event_times, title, filename):
    set_style()
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    ax1.plot(time, rho_s, color='navy')
    ax1.set_ylabel(r'$\rho_s$')
    ax1.set_title(title)
    ax1.grid(True, alpha=0.25)

    ax2.plot(time, lam_series, color='darkred')
    ax2.set_ylabel(r'$\lambda$')
    ax2.grid(True, alpha=0.25)

    ax3.eventplot(event_times, lineoffsets=0.5, linelengths=0.8, colors='black')
    ax3.set_yticks([])
    ax3.set_ylabel('Events')
    ax3.set_xlabel(r'$\tau$')

    os.makedirs('figures', exist_ok=True)
    plt.savefig(os.path.join('figures', filename))
    plt.close()


def plot_histogram(intervals, title, filename):
    set_style()
    plt.figure(figsize=(8, 4.5))
    plt.hist(intervals, bins=30, color='skyblue', edgecolor='black')
    plt.title(title)
    plt.xlabel('Inter-event interval')
    plt.ylabel('Frequency')
    os.makedirs('figures', exist_ok=True)
    plt.savefig(os.path.join('figures', filename))
    plt.close()


def plot_critical_regime_comparison(summary_rows, filename):
    set_style()
    labels = [r['name'] for r in summary_rows]
    burstiness = [r['burstiness_index'] for r in summary_rows]
    event_counts = [r['event_count'] for r in summary_rows]
    interval_var = [r['var_inter_event_interval'] for r in summary_rows]

    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))
    axes[0].bar(labels, burstiness, color='slateblue')
    axes[0].set_title('Burstiness index')
    axes[0].tick_params(axis='x', rotation=30)

    axes[1].bar(labels, event_counts, color='teal')
    axes[1].set_title('Event count')
    axes[1].tick_params(axis='x', rotation=30)

    axes[2].bar(labels, interval_var, color='darkorange')
    axes[2].set_title('Interval variance')
    axes[2].tick_params(axis='x', rotation=30)

    plt.suptitle('Critical-regime comparison across nucleation runs')
    os.makedirs('figures', exist_ok=True)
    plt.savefig(os.path.join('figures', filename))
    plt.close()
