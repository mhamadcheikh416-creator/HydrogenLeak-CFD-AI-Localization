#!/usr/bin/env python3
from pathlib import Path
import shutil, random, math
ROOT = Path(__file__).resolve().parent
CASES = ROOT/'cases'
random.seed(42)

ROOM = (8.0, 6.0, 3.0)
N_RANDOM = 100

# 20 ceiling grid sensors + 4 outlet cluster + 1 robot reference
SENSORS=[]
xs=[0.8,2.4,4.0,5.6,7.2]
ys=[0.6,2.2,3.8,5.4]
idx=1
for y in ys:
    for x in xs:
        SENSORS.append((f"S{idx:02d}_ceiling_grid",(x,y,2.80))); idx+=1
for name,pos in [
    ("S21_outlet_low",(7.65,3.0,1.40)),
    ("S22_outlet_mid",(7.65,3.0,2.10)),
    ("S23_outlet_high",(7.65,2.35,2.70)),
    ("S24_outlet_high_right",(7.65,3.65,2.70)),
    ("S25_robot_reference",(4.0,3.0,0.25)),
]:
    SENSORS.append((name,pos))

ROBOT=[]
for j,y in enumerate([0.5,1.3,2.1,2.9,3.7,4.5,5.3]):
    row=[0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5]
    if j%2: row=list(reversed(row))
    for x in row: ROBOT.append((x,y,0.25))

HEADER='''FoamFile\n{\n    version 2.0;\n    format ascii;\n    class dictionary;\n    object blockMeshDict;\n}\nscale 1;\n'''

def coords_split(v, lo, hi, eps=0.18):
    a=max(lo, v-eps); b=min(hi, v+eps)
    pts=[lo,a,b,hi]
    pts=sorted(set([round(p,4) for p in pts]))
    if len(pts)<4:
        mid=(lo+hi)/2; pts=[lo, mid-0.18, mid+0.18, hi]
    return pts

def block_mesh_dict(lx,ly):
    X=coords_split(lx,0,ROOM[0]); Y=coords_split(ly,0,ROOM[1]); Z=[0, ROOM[2]]
    verts=[]; vid={}
    for k,z in enumerate(Z):
        for j,y in enumerate(Y):
            for i,x in enumerate(X):
                vid[(i,j,k)]=len(verts); verts.append((x,y,z))
    def v(i,j,k): return vid[(i,j,k)]
    s=HEADER
    s+='vertices\n(\n' + ''.join(f'    ({x} {y} {z})\n' for x,y,z in verts) + ');\n'
    s+='blocks\n(\n'
    for j in range(3):
        for i in range(3):
            dx=X[i+1]-X[i]; dy=Y[j+1]-Y[j]
            nx=max(2,int(round(dx/0.12))); ny=max(2,int(round(dy/0.12))); nz=30
            s+=f'    hex ({v(i,j,0)} {v(i+1,j,0)} {v(i+1,j+1,0)} {v(i,j+1,0)} {v(i,j,1)} {v(i+1,j,1)} {v(i+1,j+1,1)} {v(i,j+1,1)}) ({nx} {ny} {nz}) simpleGrading (1 1 1)\n'
    s+=');\nedges ();\nboundary\n(\n'
    # inlet x=0, all three y strips
    s+='    inlet { type patch; faces (\n'
    for j in range(3): s+=f'        ({v(0,j,0)} {v(0,j+1,0)} {v(0,j+1,1)} {v(0,j,1)})\n'
    s+='    ); }\n'
    # outlet x=max
    s+='    outlet { type patch; faces (\n'
    for j in range(3): s+=f'        ({v(3,j,0)} {v(3,j,1)} {v(3,j+1,1)} {v(3,j+1,0)})\n'
    s+='    ); }\n'
    # leak is central bottom patch i=1,j=1
    s+='    leakInlet { type patch; faces (\n'
    s+=f'        ({v(1,1,0)} {v(2,1,0)} {v(2,2,0)} {v(1,2,0)})\n'
    s+='    ); }\n'
    s+='    walls { type wall; faces (\n'
    # bottom except leak
    for j in range(3):
        for i in range(3):
            if i==1 and j==1: continue
            s+=f'        ({v(i,j,0)} {v(i+1,j,0)} {v(i+1,j+1,0)} {v(i,j+1,0)})\n'
    # top
    for j in range(3):
        for i in range(3):
            s+=f'        ({v(i,j,1)} {v(i,j+1,1)} {v(i+1,j+1,1)} {v(i+1,j,1)})\n'
    # y walls
    for i in range(3):
        s+=f'        ({v(i,0,0)} {v(i,0,1)} {v(i+1,0,1)} {v(i+1,0,0)})\n'
        s+=f'        ({v(i,3,0)} {v(i+1,3,0)} {v(i+1,3,1)} {v(i,3,1)})\n'
    s+='    ); }\n);\nmergePatchPairs ();\n'
    return s

def write_files(case, lx, ly, rate, tag):
    (case/'0').mkdir(parents=True,exist_ok=True); (case/'constant').mkdir(exist_ok=True); (case/'system').mkdir(exist_ok=True)
    (case/'system/blockMeshDict').write_text(block_mesh_dict(lx,ly))
    # rate controls leak velocity and concentration injection strength (dimensionless scalar boundary remains 1)
    leak_v = {"small":0.22,"medium":0.42,"large":0.70}[rate]
    u_mean = {"small":0.045,"medium":0.060,"large":0.075}[rate]
    (case/'0/T').write_text('''FoamFile\n{\n    version 2.0;\n    format ascii;\n    class volScalarField;\n    object T;\n}\n\ndimensions [0 0 0 0 0 0 0];\ninternalField uniform 0;\nboundaryField\n{\n    inlet { type fixedValue; value uniform 0; }\n    outlet { type zeroGradient; }\n    leakInlet { type fixedValue; value uniform 1; }\n    walls { type zeroGradient; }\n}\n''')
    (case/'0/U').write_text(f'''FoamFile\n{{\n    version 2.0;\n    format ascii;\n    class volVectorField;\n    object U;\n}}\n\ndimensions [0 1 -1 0 0 0 0];\n// V4 approximation: ventilation + upward buoyancy drift for H2 cloud.\ninternalField uniform ({u_mean} 0 0.075);\nboundaryField\n{{\n    inlet {{ type fixedValue; value uniform (0.28 0 0); }}\n    outlet {{ type zeroGradient; }}\n    leakInlet {{ type fixedValue; value uniform (0 0 {leak_v}); }}\n    walls {{ type noSlip; }}\n}}\n''')
    (case/'0/p').write_text('''FoamFile\n{\n    version 2.0;\n    format ascii;\n    class volScalarField;\n    object p;\n}\n\ndimensions [0 2 -2 0 0 0 0];\ninternalField uniform 0;\nboundaryField\n{\n    inlet { type zeroGradient; } outlet { type fixedValue; value uniform 0; } leakInlet { type zeroGradient; } walls { type zeroGradient; }\n}\n''')
    probes='\n'.join(f'        ({x} {y} {z})' for _,(x,y,z) in SENSORS)
    robot='\n'.join(f'        ({x} {y} {z})' for x,y,z in ROBOT)
    (case/'system/controlDict').write_text(f'''FoamFile\n{{\n    version 2.0;\n    format ascii;\n    class dictionary;\n    object controlDict;\n}}\napplication scalarTransportFoam;\nstartFrom startTime;\nstartTime 0;\nstopAt endTime;\nendTime 300;\ndeltaT 0.05;\nwriteControl adjustableRunTime;\nwriteInterval 2;\npurgeWrite 0;\nwriteFormat ascii;\nwritePrecision 8;\nwriteCompression off;\ntimeFormat general;\ntimePrecision 6;\nrunTimeModifiable true;\nadjustTimeStep yes;\nmaxCo 0.6;\nmaxDeltaT 0.05;\nfunctions\n{{\n    fixedSensors\n    {{\n        type probes; libs ("libsampling.so"); writeControl timeStep; writeInterval 10; fields (T);\n        probeLocations\n        (\n{probes}\n        );\n    }}\n    robotPathProbes\n    {{\n        type probes; libs ("libsampling.so"); writeControl timeStep; writeInterval 20; fields (T);\n        probeLocations\n        (\n{robot}\n        );\n    }}\n}}\n''')
    (case/'system/fvSchemes').write_text('''FoamFile\n{ version 2.0; format ascii; class dictionary; object fvSchemes; }\nddtSchemes { default Euler; }\ngradSchemes { default Gauss linear; }\ndivSchemes { default none; div(phi,T) Gauss upwind; }\nlaplacianSchemes { default Gauss linear corrected; }\ninterpolationSchemes { default linear; }\nsnGradSchemes { default corrected; }\n''')
    (case/'system/fvSolution').write_text('''FoamFile\n{ version 2.0; format ascii; class dictionary; object fvSolution; }\nsolvers\n{\n    T { solver smoothSolver; smoother symGaussSeidel; tolerance 1e-08; relTol 0; }\n}\n''')
    (case/'constant/transportProperties').write_text('''FoamFile\n{ version 2.0; format ascii; class dictionary; object transportProperties; }\n// Effective hydrogen-in-air diffusivity for room-scale turbulent mixing.\nDT DT [0 2 -1 0 0 0 0] 6e-4;\n''')
    (case/'constant/g').write_text('''FoamFile\n{ version 2.0; format ascii; class uniformDimensionedVectorField; object g; }\ndimensions [0 1 -2 0 0 0 0];\nvalue (0 0 -9.81);\n''')
    (case/'LEAK_INFO.txt').write_text(f'case={case.name}\nx={lx:.3f}\ny={ly:.3f}\nz=0.000\nleak_strength={rate}\nmodel=V4 scalar transport with ventilation and upward buoyancy-drift approximation\nroom=8 x 6 x 3 m, inlet at x=0, outlet at x=8, door/window/cabinet represented in docs and visualization plan\n')

if CASES.exists(): shutil.rmtree(CASES)
CASES.mkdir()
# deterministic key scenarios
preset=[('center_floor',4.0,3.0,'medium'),('near_inlet_floor',0.8,3.0,'medium'),('near_outlet_floor',7.2,3.0,'medium'),('left_corner_floor',1.0,0.8,'small'),('right_corner_floor',7.0,5.2,'large'),('under_sensors_floor',4.8,3.5,'medium')]
case_id=1
for name,x,y,r in preset:
    c=CASES/f'leak_{case_id:03d}_{name}_{r}'; write_files(c,x,y,r,name); case_id+=1
rates=['small','medium','large']
for k in range(N_RANDOM):
    x=random.uniform(0.5,7.5); y=random.uniform(0.5,5.5); r=random.choice(rates)
    c=CASES/f'leak_{case_id:03d}_random_{r}'; write_files(c,x,y,r,'random'); case_id+=1
print(f'Generated {case_id-1} cases in {CASES}')
print('Fixed sensors:',len(SENSORS),'Robot probe points:',len(ROBOT))
