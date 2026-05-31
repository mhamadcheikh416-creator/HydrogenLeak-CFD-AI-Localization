# Hydrogen Leak CFD, Sensor Placement and AI Localization

This project studies hydrogen leak dispersion inside a ventilated 3D room using OpenFOAM and Python analysis.

## Objectives

- Simulate hydrogen leak dispersion in a room.
- Visualize hydrogen plume rise and transport toward the outlet.
- Compare fixed ceiling sensors and a mobile robot reference sensor.
- Optimize sensor placement.
- Build a CFD-generated dataset for AI-based leak localization.

## V4 Features

- 106 leak simulations.
- 25 fixed sensors.
- 56 mobile robot path probe points.
- 300 s simulation time for smoother animation.
- Sensor ranking and detection analysis.
- AI dataset generation.
- Random Forest model for leak position prediction.

## Run

```bash
chmod +x run_all_cases.sh clean_all.sh make_cases.py analysis/*.py
./run_all_cases.sh
```

Quick test:

```bash
MAX_CASES=5 ./run_all_cases.sh
```

## Results

Generated files in `results/`:

- `sensor_timeseries.csv`
- `sensor_summary.csv`
- `fixed_sensor_ranking.csv`
- `hydrogen_ai_dataset.csv`
- `ai_random_forest_metrics.csv`
- `ai_sensor_importance.csv`

## Scientific idea

Hydrogen rises because it is lighter than air and is transported by the ventilation flow. Sensors near the ceiling and outlet are expected to be the most important, while a mobile robot can provide fast local detection but lower global coverage.

## Author

Mhamad Al Sheikh
