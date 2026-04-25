"""
Native BMA 模型：原生量子基线，对比对象

基于量子振幅放大（BMA）算法的简化实现，作为量子基线。
使用五声合法步移规则。
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np

LEGAL_STATES = ["000", "001", "010", "011", "100"]
NOTE_NAMES = ["Gong", "Shang", "Jue", "Zhi", "Yu"]
NOTE_PITCHES = [60, 62, 64, 67, 69]

# WPIM参数（复用）
NOTE_PITCHES_ARRAY = np.array(NOTE_PITCHES)

def calculate_distance(i, j):
    """计算音级i到j的半音距离"""
    p_i = NOTE_PITCHES_ARRAY[i]
    p_j = NOTE_PITCHES_ARRAY[j]
    return min(abs(p_i - p_j), 12 - abs(p_i - p_j))

# 合法步移集合 Ω = {0,2,3,4,5,7,9}
LEGAL_DISTANCES = {0, 2, 3, 4, 5, 7, 9}
D = {(i, j) for i in range(5) for j in range(5) if calculate_distance(i, j) in LEGAL_DISTANCES}

BMA_NUM_QUBITS = 4
BMA_DIM = 2 ** BMA_NUM_QUBITS
BMA_PITCH_TO_STATE = {i: format(i, '04b') for i in range(5)}


def build_bma_oracle(target_states):
    diag = np.ones(BMA_DIM, dtype=complex)
    for state in target_states:
        diag[int(state, 2)] = -1
    return np.diag(diag)


def build_bma_diffusion():
    # 等价于 H^{⊗n} S H^{⊗n}，即 Grover 均值反转算子
    s = np.ones((BMA_DIM,), dtype=complex) / np.sqrt(BMA_DIM)
    return 2.0 * np.outer(s, s.conj()) - np.eye(BMA_DIM, dtype=complex)


def bma_iterations(target_count):
    if target_count <= 0:
        return 1
    return max(1, int(np.floor(0.78539816339 * np.sqrt(BMA_DIM / target_count))))


def run_bma_amplitude_remixing(target_states):
    state = np.ones((BMA_DIM,), dtype=complex) / np.sqrt(BMA_DIM)
    oracle = build_bma_oracle(target_states)
    diffusion = build_bma_diffusion()
    for _ in range(bma_iterations(len(target_states))):
        state = diffusion @ (oracle @ state)
    return np.abs(state) ** 2


def bma_target_states(current_pitch):
    allowed = [j for j in range(5) if (current_pitch, j) in D]
    return [BMA_PITCH_TO_STATE[j] for j in allowed]


def generate_native_bma_melody(length=16):
    """
    Native BMA 旋律生成：原生量子基线，使用五声合法步移。
    生成4小节（16拍）旋律。
    """
    melody = [0]
    for _ in range(length - 1):
        current = melody[-1]
        target_states = bma_target_states(current)
        probabilities = run_bma_amplitude_remixing(target_states)

        allowed = [j for j in range(5) if (current, j) in D]
        allowed_probs = np.array([probabilities[int(BMA_PITCH_TO_STATE[j], 2)] for j in allowed], dtype=float)
        if allowed_probs.sum() <= 0:
            allowed_probs = np.ones_like(allowed_probs) / len(allowed_probs)
        else:
            allowed_probs /= allowed_probs.sum()

        melody.append(int(np.random.choice(allowed, p=allowed_probs)))
    return melody


def main():
    print("=" * 60)
    print("Native BMA 模型：原生量子基线")
    print("=" * 60)
    print("\n说明：基于量子振幅放大（BMA）算法，作为量子基线对比对象。")
    print("使用五声合法步移规则。")
    print("=" * 60)

    melody = generate_native_bma_melody(32)
    print(f"生成的旋律: {' '.join(NOTE_NAMES[p] for p in melody)}")

    valid_count = sum(1 for i in range(len(melody)-1)
                      if calculate_distance(melody[i], melody[i+1]) in LEGAL_DISTANCES)
    print(f"合法步移占比: {valid_count}/{len(melody)-1} = {valid_count/(len(melody)-1)*100:.1f}%")


if __name__ == "__main__":
    main()