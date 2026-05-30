#!/usr/bin/env python3
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
summary=pd.read_csv(ROOT/'results/sensor_summary.csv')
# Features: max H2 per sensor for each case + leak strength encoded later by model script
pivot=summary.pivot_table(index=['case','leak_strength','leak_x','leak_y','leak_z'], columns='sensor_id', values='max_H2_T', aggfunc='max').reset_index()
pivot.columns=[str(c) for c in pivot.columns]
pivot=pivot.fillna(0)
pivot.to_csv(ROOT/'results/hydrogen_ai_dataset.csv', index=False)
print('Wrote hydrogen_ai_dataset.csv shape=',pivot.shape)
