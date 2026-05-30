# CFD and AI-Based Hydrogen Leak Localization in a 3D Indoor Environment

## Overview

This project presents a computational framework that combines **Computational Fluid Dynamics (CFD)** and **Artificial Intelligence (AI)** for hydrogen leak localization inside a three-dimensional indoor environment.

The objective is to simulate hydrogen dispersion, evaluate sensor network performance, generate machine-learning datasets, and estimate leak locations using data-driven models.

The long-term vision is the development of intelligent hydrogen monitoring systems and autonomous robotic platforms capable of detecting and localizing hydrogen leaks in real time.

---

## Project Highlights

* 106 hydrogen leak scenarios simulated
* OpenFOAM-based CFD framework
* 25 fixed sensors deployed
* Sensor ranking and optimization
* AI-ready dataset generation
* Random Forest leak localization model
* ParaView scientific visualization
* Foundation for future autonomous leak-detection robots

---

## Software Stack

* OpenFOAM v2412
* ParaView
* Python
* NumPy
* Pandas
* Scikit-Learn
* Random Forest Regressor

---

## Simulation Environment

The simulated environment consists of:

* 3D indoor room
* Hydrogen leak source
* Air inlet
* Air outlet
* Ceiling sensor network
* Outlet sensors
* Reference floor sensor

Hydrogen dispersion is governed by:

* Advection
* Diffusion
* Buoyancy-driven transport
* Ventilation effects

---

## Sensor Network

The monitoring system contains:

| Sensor Type      | Quantity |
| ---------------- | -------- |
| Ceiling Sensors  | 20       |
| Outlet Sensors   | 4        |
| Reference Sensor | 1        |
| Total            | 25       |

The sensor layout was designed to capture hydrogen accumulation near the ceiling due to buoyancy.

---

## CFD Dataset

Generated outputs include:

* hydrogen_ai_dataset.csv
* fixed_sensor_ranking.csv
* sensor_summary.csv
* ai_sensor_importance.csv
* ai_random_forest_metrics.csv

A total of:

* 106 leak scenarios
* 1,590,000 sensor measurements
* 30 machine-learning features

were generated.

---

## Machine Learning Results

### Random Forest Localization Performance

| Axis | MAE (m) | RMSE (m) |
| ---- | ------- | -------- |
| X    | 0.572   | 0.650    |
| Y    | 0.107   | 0.150    |
| Z    | 0.000   | 0.000    |

The AI model successfully estimates hydrogen leak locations directly from sensor measurements.

---

## Most Important Sensors Identified by AI

1. S08_ceiling_grid
2. S20_ceiling_grid
3. S05_ceiling_grid
4. S13_ceiling_grid
5. S19_ceiling_grid

These sensors are located within the hydrogen accumulation region identified by CFD simulations.

---

## Key Physical Observation

CFD simulations show that hydrogen rapidly rises due to buoyancy and accumulates near the ceiling.

This explains why ceiling-mounted sensors consistently outperform low-level sensors for leak localization.

The agreement between:

* CFD physics
* Sensor ranking analysis
* AI feature importance

is one of the strongest outcomes of this project.

---

## Future Work

Future developments include:

* Experimental validation
* Real hydrogen sensors
* Deep learning models
* Mobile robotic inspection systems
* Real-time leak localization
* Digital Twin implementation

---

## Repository Structure

```text
analysis/     Python scripts for dataset generation and AI analysis
docs/         Documentation and project reports
results/      Generated datasets and AI outputs
template/     Base OpenFOAM configuration
```

---

## Author

**Mhamad Al Sheikh**

Physics Researcher

Lebanon

2026

---

## Citation

If you use this project for research, please cite the repository and acknowledge the original work.
