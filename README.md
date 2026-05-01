# substrate-sim

# SubstrateSim Development Guide

*A Simulation Framework for Feedback-Regulated Universe Nucleation*

---

## 1. Project Overview

SubstrateSim is a scientific simulation project designed to model and analyze a feedback-regulated universe nucleation framework. The system is based on a dynamical equation governing substrate energy density and a density-dependent nucleation rate.

The goal of this project is to:

* Validate the theoretical model through simulation
* Explore parameter regimes (η, k, Γ, etc.)
* Demonstrate emergent behaviors (stability, bursts, suppression)
* Quantify deviations from Poisson processes
* Generate figures suitable for academic publication

This is a **research-grade simulation**, not just a visualization tool.

---

## 2. Core Model

### 2.1 Governing Equation

[
\frac{d\rho_s}{d\tau} = R(\rho_s) + C\lambda(\rho_s) - \Gamma(\rho_s - \rho_{eq})
]

Where:

* ( \rho_s ): substrate energy density
* ( \lambda(\rho_s) ): nucleation rate
* ( C = \eta E_u - E_n ): net energy contribution
* ( R(\rho_s) ): intrinsic generation
* ( \Gamma ): damping coefficient
* ( \rho_{eq} ): equilibrium energy

---

### 2.2 Nucleation Rate

[
\lambda(\rho_s) = \frac{\lambda_{max}}{1 + e^{-k(\rho_s - \rho_c)}}
]

Parameters:

* ( \lambda_{max} ): saturation rate
* ( \rho_c ): critical threshold
* ( k ): sensitivity

---

## 3. Development Philosophy

This project follows three principles:

### 1. Reproducibility

* Every simulation must be deterministic given a seed
* Outputs saved to disk

### 2. Modularity

* Physics logic separate from experiments
* Reusable components

### 3. Extensibility

* Designed for future:

  * spatial models
  * stochastic processes
  * visualization layers

---

## 4. Technology Stack

### Core Language

* Python 3.11+

### Required Libraries

```txt
numpy
scipy
matplotlib
pandas
```

### Optional (Later)

```txt
streamlit
scikit-learn
```

---

## 5. Project Structure

```text
substrate-sim/
│
├── README.md
├── requirements.txt
├── main.py
│
├── src/
│   ├── substrate_model.py
│   ├── nucleation.py
│   ├── spatial_grid.py
│   ├── metrics.py
│   └── plotting.py
│
├── experiments/
│   ├── low_eta_test.py
│   ├── high_k_burst_test.py
│   └── spatial_correlation_test.py
│
├── data/
├── figures/
└── logs/
```

---

## 6. Core Modules

### 6.1 substrate_model.py

Handles the dynamical system.

Responsibilities:

* Define ( \rho_s ) evolution
* Numerical integration (Euler / RK4)
* Parameter configuration

Key function:

```python
def step(rho_s, params, dt):
    return rho_s + dt * F(rho_s)
```

---

### 6.2 nucleation.py

Handles event generation.

Responsibilities:

* Compute λ(ρₛ)
* Sample stochastic events
* Return event timestamps

---

### 6.3 spatial_grid.py

Implements 2D simulation.

Responsibilities:

* Maintain grid of ρₛ(x, y)
* Apply local depletion after events
* Handle recovery/diffusion

---

### 6.4 metrics.py

Computes statistical properties.

Includes:

* nearest neighbor distances
* pair correlation function
* clustering coefficient
* event interval distributions

---

### 6.5 plotting.py

Generates figures.

Includes:

* time series plots
* phase diagrams
* spatial heatmaps
* histograms

---

## 7. Simulation Phases

---

### Phase 1: Single-Cell Dynamics

Simulate:

* ( \rho_s(\tau) )
* λ(ρₛ)
* event timeline

Goal:

* Validate equation behavior
* Confirm stability / collapse

---

### Phase 2: Threshold Behavior

Focus:

* High ( k )

Goal:

* Detect burst or avalanche behavior
* Analyze oscillations or spikes

---

### Phase 3: Spatial Simulation

Grid-based model:

* Each cell has its own ρₛ
* Local nucleation affects neighbors

Goal:

* Identify clustering
* Detect suppression zones

---

## 8. Experiments

---

### 8.1 Low Efficiency Test

Set:

```python
eta << 1
```

Expected:

* C < 0
* substrate depletion
* λ → 0

---

### 8.2 High Sensitivity Test

Set:

```python
k = large
```

Expected:

* bursts
* rapid oscillations
* threshold-triggered cascades

---

### 8.3 Spatial Correlation Test

Compare:

* constant λ
* λ(ρₛ)

Metrics:

* nearest neighbor distribution
* clustering index
* spatial variance

---

## 9. Data Output

Each run should generate:

```json
{
  "parameters": {...},
  "rho_s_time_series": [...],
  "lambda_time_series": [...],
  "event_times": [...],
  "metrics": {...}
}
```

Save to:

```text
/data/run_<timestamp>.json
```

---

## 10. Visualization Targets

Required figures:

* ρₛ vs time
* λ vs time
* event timeline
* spatial heatmap
* clustering histogram

---

## 11. Validation Strategy

Validate against:

### Analytical expectations:

* fixed points
* stability conditions

### Baseline comparison:

* Poisson model

---

## 12. Future Extensions

Planned expansions:

* stochastic noise in R(ρₛ)
* multi-scale spatial models
* 3D simulations
* adaptive time stepping
* GPU acceleration

---

## 13. Streamlit Dashboard (Later Phase)

Features:

* parameter sliders
* real-time plots
* spatial visualization
* export results

---

## 14. Development Roadmap

### Step 1

Implement single-cell model

### Step 2

Add event generation

### Step 3

Run low-η and high-k tests

### Step 4

Build spatial grid

### Step 5

Add metrics and clustering analysis

### Step 6

Generate publication figures

---

## 15. Success Criteria

The project is successful if it:

* reproduces stable equilibrium regimes
* demonstrates burst behavior at high k
* shows non-Poisson spatial structure
* produces publishable figures

---

## 16. Final Notes

This project is not just a simulation. It is:

* a validation tool for your theoretical model
* a bridge between theory and empirical analysis
* a potential contribution to computational cosmology

Keep the code clean, modular, and reproducible. The simulation is the next major step in turning your framework into a serious research contribution.
