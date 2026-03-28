# Last updated in English
#!/usr/bin/env bash
set -eu
cd "$(dirname "$0")"
# Use qiskit-env Python environment
if [ -d "./qiskit-env" ]; then
    source ./qiskit-env/bin/activate
else
    echo "Warning: qiskit-env not found in current directory, using system Python"
fi

echo "[1/3] Running comparison experiment..."
python quantum_comparison_experiment.py | tee run_comparison.log

echo "[2/3] Running pentatonic melody generator..."
python quantum_pentatonic_melody_generator.py | tee run_pentatonic.log

echo "[3/3] Testing average performance..."
python test_average.py | tee run_average.log

echo "All tests completed! Logs saved in run_*.log"
