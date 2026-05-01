# SubstrateSim Implementation Plan

This plan translates the README development roadmap into concrete, executable engineering workstreams.

## 1) Repository Bootstrapping

- Create project directories: `src/`, `experiments/`, `data/`, `figures/`, `logs/`.
- Add `requirements.txt` with pinned/min-version dependencies.
- Add `main.py` entrypoint with CLI options:
  - `--mode` (`single-cell`, `spatial`, `experiment`)
  - `--experiment` (named experiment runner)
  - `--seed` (deterministic runs)
  - `--output` (result path override)
- Add base run config schema (dict/dataclass) for all simulation parameters.

## 2) Core Physics Module (`src/substrate_model.py`)

- Implement model primitives:
  - `intrinsic_generation(rho_s, params)` for `R(rho_s)`
  - `nucleation_feedback_term(rho_s, params)` for `C * lambda(rho_s)`
  - `damping_term(rho_s, params)` for `-Gamma*(rho_s-rho_eq)`
  - `drho_dt(rho_s, params)` combining all terms
- Implement integrators:
  - Euler step
  - RK4 step (default for analysis-grade stability)
- Add `simulate_single_cell(...)` returning full time series:
  - `time`, `rho_s`, `lambda`, `events`
- Add deterministic RNG plumbing (`numpy.random.Generator`).

## 3) Nucleation/Event Module (`src/nucleation.py`)

- Implement sigmoid nucleation rate function:
  - `lambda_rate(rho_s, lambda_max, rho_c, k)`
- Implement event sampling per timestep:
  - Bernoulli approximation for small `dt`
  - Optional Poisson sampling for robustness checks
- Add event timeline utilities:
  - event indices/timestamps extraction
  - event count per window

## 4) Experiments Phase I–II (`experiments/`)

- Implement baseline single-cell run script.
- Implement `low_eta_test.py`:
  - sweep `eta` in low regime
  - verify depletion and suppression (`lambda -> 0` trend)
- Implement `high_k_burst_test.py`:
  - sweep large `k`
  - detect burst-like signatures (peaks/spikes in lambda and event rate)
- Standardize outputs:
  - one JSON per run
  - summary CSV for parameter sweep comparison

## 5) Spatial Simulation Module (`src/spatial_grid.py`)

- Represent 2D field `rho_s[x, y]`.
- Per-cell update loop:
  - local `drho_dt`
  - per-cell nucleation sampling
- Add local event depletion kernel and neighbor coupling.
- Add optional diffusion/recovery term.
- Implement `simulate_spatial(...)` with snapshots + event map outputs.

## 6) Metrics Module (`src/metrics.py`)

- Implement temporal metrics:
  - inter-event interval distribution
  - burstiness index
- Implement spatial metrics:
  - nearest-neighbor distances
  - clustering coefficient surrogate
  - pair-correlation/radial statistics (first practical version)
  - spatial variance map summaries
- Implement baseline comparator utilities (constant-rate Poisson surrogate).

## 7) Plotting Module (`src/plotting.py`)

- Implement reusable plotting functions for:
  - `rho_s vs time`
  - `lambda vs time`
  - raster/event timeline
  - spatial heatmap snapshots
  - histogram/distribution plots for clustering and intervals
- Add style presets suitable for publication figures.
- Save all figures under `figures/` with deterministic naming.

## 8) Data/Logging/Reproducibility Standards

- Save run artifact structure per README:
  - parameters
  - time series
  - event times
  - computed metrics
- Filename convention: `data/run_<timestamp>_<mode>_<seed>.json`.
- Add `logs/` run summaries (human-readable) and errors.
- Ensure every executable path accepts explicit seed and persists it in output.

## 9) Validation Framework

- Add validation checks for:
  - numerical stability across `dt`
  - fixed-point behavior in stable regimes
  - suppression behavior in expected low-efficiency regimes
- Add baseline comparison scripts against constant-`lambda` Poisson process.
- Define pass/fail heuristics for each experiment in code comments + docs.

## 10) Delivery Sequence (Milestones)

1. **M1 – Scaffolding + single-cell engine**
   - complete sections 1–3 and baseline run
2. **M2 – Phase I/II experiments**
   - complete section 4 with sweep outputs
3. **M3 – Spatial engine**
   - complete section 5 with basic 2D runs
4. **M4 – Metrics + validation**
   - complete sections 6 and 9
5. **M5 – Publication plots + polish**
   - complete sections 7 and 8

## 11) Definition of Done

A milestone is done when:

- Code module is implemented and callable from `main.py`.
- At least one deterministic run artifact is generated in `data/`.
- Corresponding figures are generated in `figures/`.
- Metrics are computed and serialized.
- A short experiment note is added to logs with observed behavior.

## 12) Immediate Next Actions

- [ ] Create folder structure and placeholder modules.
- [ ] Add requirements + CLI entrypoint.
- [ ] Implement and test single-cell `drho_dt` + RK4 integration.
- [ ] Implement sigmoid nucleation and event sampling.
- [ ] Run first baseline simulation and emit JSON + 3 core plots.
