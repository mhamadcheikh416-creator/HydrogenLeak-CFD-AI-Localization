#!/bin/bash
set -e
cd "$(dirname "$0")"
mkdir -p results
if [ ! -d cases ]; then
  python3 make_cases.py
fi
MAX_CASES=${MAX_CASES:-106}
COUNT=0
for c in cases/leak_*; do
    COUNT=$((COUNT+1))
    if [ "$COUNT" -gt "$MAX_CASES" ]; then break; fi
    echo "========================================"
    echo "Running $c"
    echo "========================================"
    ( cd "$c" && blockMesh > log.blockMesh && scalarTransportFoam > log.scalarTransportFoam )
    touch "$c/Room_H2.foam"
done
python3 analysis/extract_sensor_data.py
python3 analysis/rank_sensors.py
python3 analysis/build_ai_dataset.py
python3 analysis/train_random_forest.py || true
python3 analysis/make_root_optional.py || true
echo "Done. Results are in results/. Open cases/.../Room_H2.foam in ParaView and color by T."
