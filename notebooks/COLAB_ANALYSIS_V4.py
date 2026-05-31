# Google Colab analysis for HydrogenLeak_Room_Study_V4
from google.colab import files
import pandas as pd
import matplotlib.pyplot as plt
import glob, os

print('Upload these files from results/:')
print('fixed_sensor_ranking.csv, sensor_summary.csv, sensor_timeseries.csv, hydrogen_ai_dataset.csv')
files.upload()

def f(pattern):
    m=glob.glob(pattern)
    if not m: raise FileNotFoundError(pattern)
    return m[0]

ranking=pd.read_csv(f('*fixed_sensor_ranking*.csv'))
summary=pd.read_csv(f('*sensor_summary*.csv'))
times=pd.read_csv(f('*sensor_timeseries*.csv'))

display(ranking.sort_values('score', ascending=False).head(15))

plt.figure(figsize=(14,6))
r=ranking.sort_values('score', ascending=False)
plt.bar(r['sensor_id'], r['score']); plt.xticks(rotation=75); plt.title('V4 sensor ranking'); plt.ylabel('score'); plt.grid(axis='y'); plt.show()

plt.figure(figsize=(14,6))
r=ranking.sort_values('coverage', ascending=False)
plt.bar(r['sensor_id'], r['coverage']); plt.xticks(rotation=75); plt.title('V4 sensor coverage'); plt.ylabel('coverage'); plt.grid(axis='y'); plt.show()

plt.figure(figsize=(14,6))
r=ranking.sort_values('avg_detection_time')
plt.bar(r['sensor_id'], r['avg_detection_time']); plt.xticks(rotation=75); plt.title('V4 average detection time'); plt.ylabel('s'); plt.grid(axis='y'); plt.show()

case=times['case'].unique()[0]
sub=times[times['case']==case]
plt.figure(figsize=(14,7))
for sid,g in sub.groupby('sensor_id'):
    plt.plot(g['time'], g['H2_concentration_T'], label=sid)
plt.title('H2 concentration vs time - '+case); plt.xlabel('time (s)'); plt.ylabel('T = H2 concentration proxy'); plt.legend(fontsize=7, ncol=3); plt.grid(); plt.show()

valid=summary.dropna(subset=['detection_time_threshold_0p01'])
best=valid.loc[valid.groupby('case')['detection_time_threshold_0p01'].idxmin()]
display(best[['case','leak_strength','sensor_id','detection_time_threshold_0p01','max_H2_T']].head(30))

print('Best global sensor:', ranking.sort_values('score', ascending=False).iloc[0]['sensor_id'])
