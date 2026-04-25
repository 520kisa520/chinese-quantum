"""
Rule-based 模型：传统硬规则方法

基于五声合法步移的硬规则生成，作为传统方法对比。
"""

import random
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


def generate_rule_based_melody(length=16):
    """
    Rule-based 旋律生成：传统硬规则方法，只选择合法邻居。
    生成4小节（16拍）旋律。
    """
    melody = [0]
    for _ in range(length - 1):
        neighbors = [j for j in range(5) if (melody[-1], j) in D]
        if not neighbors:
            neighbors = [melody[-1]]
        melody.append(random.choice(neighbors))
    return melody


def main():
    print("=" * 60)
    print("Rule-based 模型：传统硬规则方法")
    print("=" * 60)
    print("\n说明：基于五声合法步移的硬规则生成，作为传统方法对比。")
    print("只选择当前音级的合法邻居。")
    print("=" * 60)

    melody = generate_rule_based_melody(32)
    print(f"生成的旋律: {' '.join(NOTE_NAMES[p] for p in melody)}")

    valid_count = sum(1 for i in range(len(melody)-1)
                      if calculate_distance(melody[i], melody[i+1]) in LEGAL_DISTANCES)
    print(f"合法步移占比: {valid_count}/{len(melody)-1} = {valid_count/(len(melody)-1)*100:.1f}%")


if __name__ == "__main__":
    main()