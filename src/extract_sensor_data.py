#!/usr/bin/env python3
from pathlib import Path
import csv, re, math
ROOT=Path(__file__).resolve().parents[1]
# Must match make_cases.py
SENSORS=[]
xs=[0.8,2.4,4.0,5.6,7.2]; ys=[0.6,2.2,3.8,5.4]
idx=1
for y in ys:
    for x in xs:
        SENSORS.append((f"S{idx:02d}_ceiling_grid",(x,y,2.80))); idx+=1
for name,pos in [("S21_outlet_low",(7.65,3.0,1.40)),("S22_outlet_mid",(7.65,3.0,2.10)),("S23_outlet_high",(7.65,2.35,2.70)),("S24_outlet_high_right",(7.65,3.65,2.70)),("S25_robot_reference",(4.0,3.0,0.25))]:
    SENSORS.append((name,pos))

def leak_info(case):
    txt=(case/'LEAK_INFO.txt').read_text(errors='ignore') if (case/'LEAK_INFO.txt').exists() else ''
    def grab(key, default=''):
        m=re.search(rf'{key}=([^\n]+)', txt); return m.group(1).strip() if m else default
    return float(grab('x','nan')), float(grab('y','nan')), float(grab('z','0')), grab('leak_strength','unknown')

def parse_probe_file(p):
    rows=[]
    if not p.exists(): return rows
    for line in p.read_text(errors='ignore').splitlines():
        line=line.strip()
        if not line or line.startswith('#'): continue
        nums=[float(x) for x in re.findall(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?', line)]
        if len(nums)>=2: rows.append((nums[0], nums[1:]))
    return rows

out=ROOT/'results'; out.mkdir(exist_ok=True)
allrows=[]; summary=[]; TH=0.01
for case in sorted((ROOT/'cases').glob('leak_*')):
    lx,ly,lz,strength=leak_info(case)
    pf=case/'postProcessing/fixedSensors/0/T'
    data=parse_probe_file(pf)
    if not data:
        print('Missing or empty fixed probe file:',pf); continue
    maxvals=[0.0]*len(SENSORS); det=[None]*len(SENSORS)
    for t,vals in data:
        for i,v in enumerate(vals[:len(SENSORS)]):
            if v>maxvals[i]: maxvals[i]=v
            if det[i] is None and v>=TH: det[i]=t
            sx,sy,sz=SENSORS[i][1]
            allrows.append([case.name,strength,t,SENSORS[i][0],sx,sy,sz,lx,ly,lz,v])
    valid=[i for i,d in enumerate(det) if d is not None]
    best_i=min(valid, key=lambda i: det[i]) if valid else None
    for i,(sid,(sx,sy,sz)) in enumerate(SENSORS):
        dist=math.sqrt((sx-lx)**2+(sy-ly)**2+(sz-lz)**2)
        summary.append([case.name,strength,lx,ly,lz,sid,sx,sy,sz,dist,det[i] if det[i] is not None else '',maxvals[i], 'YES' if i==best_i else ''])
with open(out/'sensor_timeseries.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['case','leak_strength','time','sensor_id','sensor_x','sensor_y','sensor_z','leak_x','leak_y','leak_z','H2_concentration_T']); w.writerows(allrows)
with open(out/'sensor_summary.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['case','leak_strength','leak_x','leak_y','leak_z','sensor_id','sensor_x','sensor_y','sensor_z','distance_to_leak','detection_time_threshold_0p01','max_H2_T','first_detector']); w.writerows(summary)
print('Wrote sensor_timeseries.csv rows=',len(allrows)); print('Wrote sensor_summary.csv rows=',len(summary))
