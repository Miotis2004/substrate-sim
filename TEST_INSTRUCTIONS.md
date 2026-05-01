# Test Instructions for SubstrateSim

This document provides instructions on how to set up the environment, run the simulation tests, validate the outputs, and generate plots.

## 1. Environment Setup

Ensure you are using Python 3.11+. The project relies on specific packages for numerics and plotting.

Install the requirements:

```bash
pip install -r requirements.txt
```

## 2. Running Simulations (Data Generation)

Before validating or plotting, you need to generate simulation data. The outputs will be saved in the `data/` directory.

### Single-Cell Baseline

```bash
python main.py --mode single-cell --seed 42
```

### Spatial Simulation

```bash
python main.py --mode spatial --seed 42
```

### Low Efficiency Experiment

```bash
python main.py --mode experiment --experiment low_eta --seed 42
```

### High k (Burst) Experiment

```bash
python main.py --mode experiment --experiment high_k --seed 42
```

## 3. Validating the Results

The metrics module contains tests to check if the generated simulations reached stability and to output the burstiness index of the series.

To run the validation step on all `.json` files inside the `data/` directory, use:

```bash
PYTHONPATH=. python experiments/validate.py
```

*Note: Ensure the data is generated first.*

## 4. Generating Publication Plots

To generate the final visualizations (timeseries plots, spatial snapshots, and inter-event interval histograms) from the generated datasets, run the plotting script. The plots will be saved to the `figures/` directory.

```bash
PYTHONPATH=. python src/plotting.py
```

You can then inspect the generated `.png` files in the `figures/` directory.
