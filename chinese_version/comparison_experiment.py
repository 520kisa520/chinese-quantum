#!/usr/bin/env python3
"""
对照实验：验证量子方案优势

实验设置：
1. 纯随机基线：8个态均匀随机，理论合法率62.5%
2. 经典随机游走：8个音的拓扑随机游走
3. 量子Grover：翻转合法态相位，放大合法态振幅

关键修正：
- 使用论文的正确编码（论文表2）
- Grover预言机翻转合法态（不是非法态）
"""

import random
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

legal_states = ["000", "001", "010", "011", "100"]
illegal_states = ["101", "110", "111"]
all_states = legal_states + illegal_states

pos_to_code = {
    0: "000", 1: "001", 2: "010", 3: "011", 4: "100",
    5: "101", 6: "110", 7: "111"
}


def classical_random_walk(steps=16):
    """经典随机游走 - 8个音的拓扑"""
    position = 0
    for _ in range(steps):
        if random.random() < 0.5:
            position = (position + 1) % 8
        else:
            position = (position - 1) % 8
    return pos_to_code[position]


def run_classical_experiment(trials=1024):
    """运行经典随机游走实验"""
    counts = {}
    for _ in range(trials):
        result = classical_random_walk(16)
        counts[result] = counts.get(result, 0) + 1

    total = sum(counts.values())
    legal_total = sum(counts.get(s, 0) for s in legal_states)
    legal_ratio = legal_total / total * 100

    return counts, legal_ratio


def add_phase_flip(qc, target_code):
    """翻转合法目标态的相位"""
    flip_bits = []
    for i, bit in enumerate(reversed(target_code)):
        if bit == '0':
            flip_bits.append(i)

    if flip_bits:
        qc.x(flip_bits)
    qc.h(2)
    qc.ccx(0, 1, 2)
    qc.h(2)
    if flip_bits:
        qc.x(flip_bits)
    qc.barrier()
    return qc


def build_grover_oracle(qc):
    """Grover预言机 - 翻转所有合法态相位"""
    for code in legal_states:
        qc = add_phase_flip(qc, code)
    return qc


def build_grover_diffusion(qc):
    """Grover扩散算子"""
    qc.h([0, 1, 2])
    qc.x([0, 1, 2])
    qc.h(2)
    qc.ccx(0, 1, 2)
    qc.h(2)
    qc.x([0, 1, 2])
    qc.h([0, 1, 2])
    qc.barrier()
    return qc


def run_quantum_grover_experiment(Ko, shots=1024):
    """运行量子Grover实验"""
    qc = QuantumCircuit(3, 3)
    qc.h([0, 1, 2])
    qc.barrier()

    for _ in range(Ko):
        qc = build_grover_oracle(qc)
        qc = build_grover_diffusion(qc)

    qc.measure([0, 1, 2], [0, 1, 2])

    simulator = AerSimulator()
    result = simulator.run(qc, shots=shots).result()
    counts = result.get_counts()

    total = sum(counts.values())
    legal_total = sum(counts.get(s, 0) for s in legal_states)
    legal_ratio = legal_total / total * 100

    return counts, legal_ratio


def run_pure_random_experiment(trials=1024):
    """纯随机基线实验"""
    counts = {}
    for _ in range(trials):
        result = random.choice(all_states)
        counts[result] = counts.get(result, 0) + 1

    total = sum(counts.values())
    legal_total = sum(counts.get(s, 0) for s in legal_states)
    legal_ratio = legal_total / total * 100

    return counts, legal_ratio


if __name__ == "__main__":
    print("=" * 80)
    print("对照实验：验证量子方案优势")
    print("=" * 80)
    print()
    print(f"合法态（论文表2）: {legal_states}")
    print(f"非法态（论文表2）: {illegal_states}")
    print(f"理论基线: {len(legal_states)}/8 = {len(legal_states)/8*100:.1f}%")
    print()

    pure_counts, pure_ratio = run_pure_random_experiment(1024)
    print("[1] 纯随机基线:")
    print(f"    合法态占比: {pure_ratio:.1f}%")

    c_counts, c_ratio = run_classical_experiment(1024)
    print("[2] 经典随机游走（8音拓扑）:")
    print(f"    合法态占比: {c_ratio:.1f}%")
    print(f"    提升vs纯随机: {c_ratio - pure_ratio:+.1f}%")

    q1_counts, q1_ratio = run_quantum_grover_experiment(Ko=1, shots=1024)
    print("[3] 量子Grover（Ko=1）:")
    print(f"    合法态占比: {q1_ratio:.1f}%")
    print(f"    提升vs经典: {q1_ratio - c_ratio:+.1f}%")

    q2_counts, q2_ratio = run_quantum_grover_experiment(Ko=2, shots=1024)
    print("[4] 量子Grover（Ko=2）:")
    print(f"    合法态占比: {q2_ratio:.1f}%")
    print(f"    提升vs经典: {q2_ratio - c_ratio:+.1f}%")

    print()
    print("=" * 80)
    print("【总结对比】")
    print(f"{'方法':<35} {'合法态占比':>12} {'vs纯随机':>15}")
    print("-" * 80)
    print(f"{'纯随机基线':<35} {pure_ratio:>11.1f}% {(pure_ratio-62.5):+14.1f}%")
    print(f"{'经典随机游走':<35} {c_ratio:>11.1f}% {(c_ratio-62.5):+14.1f}%")
    print(f"{'量子Grover(Ko=1)':<35} {q1_ratio:>11.1f}% {(q1_ratio-62.5):+14.1f}%")
    print(f"{'量子Grover(Ko=2)':<35} {q2_ratio:>11.1f}% {(q2_ratio-62.5):+14.1f}%")
    print("=" * 80)
    print()
    print("【与论文结果对比】")
    print("  论文本文方法五声合规率: 98.7%")
    print(f"  量子Grover(Ko=2)实验结果: {q2_ratio:.1f}%")
    print(f"  差异: {abs(q2_ratio - 98.7):.1f}%")
    print()
    if q2_ratio > 95:
        print("✓ 量子Grover约束有效！")
        print("  结果接近论文预期(98.7%)，算法实现正确。")
