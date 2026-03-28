# Last updated in English
#!/usr/bin/env bash
set -eu
cd "$(dirname "$0")"
# 使用 qiskit-env 的 Python 环境
source ./qiskit-env/bin/activate

echo "[1/2] 运行 comparison_experiment.py"
./qiskit-env/bin/python comparison_experiment.py | tee run_comparison.log

echo "[2/2] 运行 pentatonic_melody.py"
./qiskit-env/bin/python pentatonic_melody.py | tee run_pentatonic.log

echo "全部运行完成，日志保存在 run_*.log"