#!/bin/bash
set -e
cd "$(dirname "$0")"
find cases -maxdepth 2 -type d -regex '.*/[0-9]+\(\.[0-9]+\)?' -not -name 0 -exec rm -rf {} + 2>/dev/null || true
find cases -name 'log.*' -delete 2>/dev/null || true
find cases -name '*.foam' -delete 2>/dev/null || true
rm -rf results/*
echo "Cleaned generated OpenFOAM time folders, logs, foam markers and results."
