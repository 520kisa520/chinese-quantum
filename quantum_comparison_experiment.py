#!/usr/bin/env python3
"""
Quantum Comparison Experiment
Experiment Setup:
1. Pure random baseline: 8 states uniform random, theoretical legal rate 62.5%
2. Classical random walk: 8-note topology random walk
3. Quantum Grover: Flip legal state phase, amplify legal state amplitude

Key Modifications:
- Uses paper's correct encoding (Table 2)
- Grover oracle flips legal states, not illegal ones
"""

import random
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

LEGAL_STATES = ["000", "001", "010", "011", "100"]
ILLEGAL_STATES = ["101", "110", "111"]
ALL_STATES = LEGAL_STATES + ILLEGAL_STATES

POS_TO_CODE = {
    0: "000", 1: "001", 2: "010", 3: "011", 4: "100",
    5: "101", 6: "110", 7: "111"
}


def classical_random_walk(steps=16):
    """Classical random walk - 8-note topology"""
    position = 0
    for _ in range(steps):
        if random.random() < 0.5:
            position = (position + 1) % 8
        else:
            position = (position - 1) % 8
    return POS_TO_CODE[position]


def run_classical_experiment(trials=1024):
    """Run classical random walk experiment"""
    counts = {}
    for _ in range(trials):
        result = classical_random_walk(16)
        counts[result] = counts.get(result, 0) + 1

    total = sum(counts.values())
    legal_total = sum(counts.get(s, 0) for s in LEGAL_STATES)
    legal_ratio = legal_total / total * 100

    return counts, legal_ratio


def add_phase_flip(qc, target_code):
    """Flip phase of legal target state"""
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
    """Grover oracle - flip all legal states phase"""
    for code in LEGAL_STATES:
        qc = add_phase_flip(qc, code)
    return qc


def build_grover_diffusion(qc):
    """Grover diffusion operator"""
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
    """Run quantum Grover experiment"""
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
    legal_total = sum(counts.get(s, 0) for s in LEGAL_STATES)
    legal_ratio = legal_total / total * 100

    return counts, legal_ratio


def run_pure_random_experiment(trials=1024):
    """Run pure random experiment"""
    counts = {}
    for _ in range(trials):
        result = random.choice(ALL_STATES)
        counts[result] = counts.get(result, 0) + 1

    total = sum(counts.values())
    legal_total = sum(counts.get(s, 0) for s in LEGAL_STATES)
    legal_ratio = legal_total / total * 100

    return counts, legal_ratio


if __name__ == "__main__":
    print("=" * 80)
    print("Quantum Comparison Experiment")
    print("=" * 80)
    print()
    print(f"Legal states (Paper Table 2): {LEGAL_STATES}")
    print(f"Illegal states (Paper Table 2): {ILLEGAL_STATES}")
    print(f"Theoretical baseline: {len(LEGAL_STATES)}/8 = {len(LEGAL_STATES)/8*100:.1f}%")
    print()

    pure_counts, pure_ratio = run_pure_random_experiment(1024)
    print("[1] Pure random baseline:")
    print(f"    Legal ratio: {pure_ratio:.1f}%")

    c_counts, c_ratio = run_classical_experiment(1024)
    print("[2] Classical random walk (8-note topology):")
    print(f"    Legal ratio: {c_ratio:.1f}%")
    print(f"    Improvement vs pure random: {c_ratio - pure_ratio:+.1f}%")

    q1_counts, q1_ratio = run_quantum_grover_experiment(Ko=1, shots=1024)
    print("[3] Quantum Grover (Ko=1):")
    print(f"    Legal ratio: {q1_ratio:.1f}%")
    print(f"    Improvement vs classical: {q1_ratio - c_ratio:+.1f}%")

    q2_counts, q2_ratio = run_quantum_grover_experiment(Ko=2, shots=1024)
    print("[4] Quantum Grover (Ko=2):")
    print(f"    Legal ratio: {q2_ratio:.1f}%")
    print(f"    Improvement vs classical: {q2_ratio - c_ratio:+.1f}%")

    print()
    print("=" * 80)
    print("Summary Comparison")
    print(f"{'Method':<35} {'Legal Ratio':>12} {'vs Pure Random':>15}")
    print("-" * 80)
    print(f"{'Pure Random':<35} {pure_ratio:>11.1f}% {(pure_ratio-62.5):+14.1f}%")
    print(f"{'Classical Random Walk':<35} {c_ratio:>11.1f}% {(c_ratio-62.5):+14.1f}%")
    print(f"{'Quantum Grover (Ko=1)':<35} {q1_ratio:>11.1f}% {(q1_ratio-62.5):+14.1f}%")
    print(f"{'Quantum Grover (Ko=2)':<35} {q2_ratio:>11.1f}% {(q2_ratio-62.5):+14.1f}%")
    print("=" * 80)
    print()
    print("Comparison with Paper Results")
    print("  Paper claimed method pentatonic compliance rate: 98.7%")
    print(f"  Quantum Grover (Ko=2) experimental result: {q2_ratio:.1f}%")
    print(f"  Difference: {abs(q2_ratio - 98.7):.1f}%")
    print()
    if q2_ratio > 95:
        print("✓ Quantum Grover constraint is effective!")
        print("  Results are close to paper's expected 98.7%, algorithm implementation is correct.")
