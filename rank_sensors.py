#!/usr/bin/env python3
from pathlib import Path
import csv, statistics, math
ROOT=Path(__file__).resolve().parents[1]
rows=list(csv.DictReader(open(ROOT/'results/sensor_summary.csv')))
by={}
for r in rows:
    sid=r['sensor_id']; by.setdefault(sid,{'det':[],'max':[],'first':0,'n':0,'dist':[]})
    by[sid]['n']+=1
    if r['detection_time_threshold_0p01']!='': by[sid]['det'].append(float(r['detection_time_threshold_0p01']))
    by[sid]['max'].append(float(r['max_H2_T']))
    by[sid]['dist'].append(float(r['distance_to_leak']))
    if r['first_detector']=='YES': by[sid]['first']+=1
out=[]
for sid,d in by.items():
    avg=statistics.mean(d['det']) if d['det'] else 999999
    med=statistics.median(d['det']) if d['det'] else 999999
    coverage=len(d['det'])/d['n'] if d['n'] else 0
    avgmax=statistics.mean(d['max']) if d['max'] else 0
    avgdist=statistics.mean(d['dist']) if d['dist'] else 0
    score=coverage*1000 + d['first']*35 + math.log10(avgmax+1e-12)*10 - avg*0.7
    out.append([sid,d['n'],len(d['det']),coverage,avg,med,d['first'],avgmax,avgdist,score])
out.sort(key=lambda x:x[-1], reverse=True)
with open(ROOT/'results/fixed_sensor_ranking.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['sensor_id','n_cases','n_detected','coverage','avg_detection_time','median_detection_time','first_detector_count','avg_max_H2','avg_distance_to_leak','score']); w.writerows(out)
print('Wrote fixed_sensor_ranking.csv')
