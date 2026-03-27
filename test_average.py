#!/usr/bin/env python3
"""
Test Average Performance
Run 10 independent experiments and calculate statistics
"""

from quantum_pentatonic_melody_generator import run_global_grover
from quantum_comparison_experiment import run_quantum_grover_experiment


def test_avg_grover():
    """Test average Grover measurement performance"""
    print("=== Running 10 independent Grover measurements ===")
    
    legal_ratios = []
    for i in range(10):
        counts = run_global_grover(1024)
        legal = sum(counts.get(code, 0) for code in ["000", "001", "010", "011", "100"])
        total = sum(counts.values())
        ratio = legal / total * 100
        legal_ratios.append(ratio)
        print(f"Run {i+1} : {ratio:.1f}%")
    
    avg = sum(legal_ratios) / len(legal_ratios)
    std = (sum((x - avg) ** 2 for x in legal_ratios) / len(legal_ratios)) ** 0.5
    
    print(f"\nAverage: {avg:.1f}%")
    print(f"Standard Deviation: {std:.2f}%")
    print(f"Range: {min(legal_ratios):.1f}% - {max(legal_ratios):.1f}%")


def test_avg_comparison():
    """Test average comparison experiment performance"""
    print("\n=== Average comparison experiment ===")
    
    ko2_ratios = []
    for i in range(10):
        _, ratio = run_quantum_grover_experiment(2)
        ko2_ratios.append(ratio)
        print(f"Ko=2, run {i+1}: {ratio:.1f}%")
    
    avg_ko2 = sum(ko2_ratios) / len(ko2_ratios)
    std_ko2 = (sum((x - avg_ko2) ** 2 for x in ko2_ratios) / len(ko2_ratios)) ** 0.5
    
    print(f"\nKo=2 Average: {avg_ko2:.1f}%")
    print(f"Ko=2 Standard Deviation: {std_ko2:.2f}%")
    print(f"Ko=2 Range: {min(ko2_ratios):.1f}% - {max(ko2_ratios):.1f}%")


if __name__ == "__main__":
    test_avg_grover()
    test_avg_comparison()
