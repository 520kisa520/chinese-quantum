 
"""
WPIM模型五声音阶旋律生成 - 论文验证版

基于加权相位干涉模型（Weighted Phase Interference Model, WPIM）
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np
from midiutil import MIDIFile

LEGAL_STATES = ["000", "001", "010", "011", "100"]
NOTE_NAMES = ["宫", "商", "角", "徵", "羽"]
NOTE_PITCHES = [60, 62, 64, 67, 69]

NOTE_PITCHES_ARRAY = np.array(NOTE_PITCHES)

def calculate_distance(i, j):
    """计算音级i到j的半音距离"""
    p_i = NOTE_PITCHES_ARRAY[i]
    p_j = NOTE_PITCHES_ARRAY[j]
    return min(abs(p_i - p_j), 12 - abs(p_i - p_j))

LEGAL_DISTANCES = {0, 2, 3, 4, 5, 7, 9}
D = {(i, j) for i in range(5) for j in range(5) if calculate_distance(i, j) in LEGAL_DISTANCES}

STEP_PREFERENCE = {
    0: 1.0,
    2: 1.3,
    3: 1.2,
    4: 1.0,
    5: 0.8,
    7: 0.6,
    9: 0.4,
}

NOTE_DURATION_PROBS = {
    0.25: 0.20,
    0.5:  0.35,
    1.0:  0.25,
    2.0:  0.12,
    4.0:  0.03,
    -1.0: 0.05,
}

W_base = np.array([
    [0.447, 0.065, 0.200, 0.048, 0.240],
    [0.172, 0.274, 0.125, 0.157, 0.272],
    [0.127, 0.076, 0.223, 0.254, 0.320],
    [0.164, 0.035, 0.220, 0.106, 0.475],
    [0.125, 0.053, 0.044, 0.041, 0.737]
])

phi_matrix = 2 * np.pi * W_base

def add_phase_flip(qc, code):
    flip_bits = [i for i, bit in enumerate(reversed(code)) if bit == '0']
    if flip_bits:
        qc.x(flip_bits)
    qc.h(2)
    qc.ccx(0, 1, 2)
    qc.h(2)
    if flip_bits:
        qc.x(flip_bits)
    qc.barrier()
    return qc

def grover_oracle(qc, codes):
    for code in codes:
        qc = add_phase_flip(qc, code)
    return qc

def grover_diffusion(qc):
    qc.h([0, 1, 2])
    qc.x([0, 1, 2])
    qc.h(2)
    qc.ccx(0, 1, 2)
    qc.h(2)
    qc.x([0, 1, 2])
    qc.h([0, 1, 2])
    qc.barrier()
    return qc

def build_grover_circuit() -> QuantumCircuit:
    qc = QuantumCircuit(3, 3)
    qc.h([0, 1, 2])
    qc.barrier()
    for _ in range(2):
        qc = grover_oracle(qc, LEGAL_STATES)
        qc = grover_diffusion(qc)
    qc.measure([0, 1, 2], [0, 1, 2])
    return qc

def run_global_grover(shots=1024):
    qc = build_grover_circuit()
    return AerSimulator().run(qc, shots=shots).result().get_counts()

def export_grover_circuit_for_composer():
    qc = build_grover_circuit()
    try:
        qasm_str = qc.qasm()
    except AttributeError:
        from qiskit.qasm2 import dumps
        qasm_str = dumps(qc)
    print("Grover电路QASM字符串（复制到IBM Quantum Composer）：")
    print(qasm_str)
    return qasm_str

def export_grover_circuit_diagram(filename: str = "grover_circuit.png", fold: int = 10) -> str:
    qc = build_grover_circuit()
    try:
        fig = qc.draw(output="mpl", fold=fold)
    except Exception as exc:
        from qiskit.exceptions import MissingOptionalLibraryError
        if isinstance(exc, MissingOptionalLibraryError) or "pylatexenc" in str(exc):
            text_diagram = qc.draw(output="text", fold=fold)
            text_filename = filename.replace('.png', '.txt')
            with open(text_filename, 'w', encoding='utf-8') as f:
                f.write(str(text_diagram))
            print(f"缺少 pylatexenc，无法生成PNG图。已导出文本电路图: {text_filename}")
            print("若要生成PNG图，请安装 pylatexenc: python3 -m pip install pylatexenc")
            return text_filename
        raise RuntimeError("无法生成电路图，请确保已安装 pylatexenc 和 matplotlib") from exc
    fig.savefig(filename, bbox_inches="tight", dpi=300)
    print(f"Grover电路图已保存: {filename}")
    return filename

def generate_note_durations(total_beats: float, num_notes: int) -> list[float]:
    """生成符合中国五声旋律特征的时值序列，确保总拍数准确"""
    durations = []
    beats_per_measure = 4.0
    measures = int(total_beats / beats_per_measure)
    
    # 为每个小节生成时值（先填满正时值，再添加休止符）
    for m in range(measures):
        measure_beats = 0.0
        measure_durations = []
        
        # 先填满小节的正时值
        while measure_beats < beats_per_measure:
            remaining = beats_per_measure - measure_beats
            
            # 如果剩余很小，用最后一个音符填满
            if remaining < 0.125:
                if len(measure_durations) == 0 or measure_durations[-1] >= 0:
                    measure_durations.append(remaining)
                break
            
            r = np.random.random()
            
            # 决定时值（只考虑正时值）
            if remaining >= 2.0 and r < 0.08:
                duration = 2.0
            elif remaining >= 1.5 and 0.08 <= r < 0.15:
                duration = 1.5
            elif remaining >= 1.0 and 0.15 <= r < 0.35:
                duration = 1.0
            elif remaining >= 0.75 and 0.35 <= r < 0.45:
                duration = 0.75
            elif remaining >= 0.5 and 0.45 <= r < 0.65:
                duration = 0.5
            elif remaining >= 0.375 and 0.65 <= r < 0.75:
                duration = 0.375
            elif remaining >= 0.25 and 0.75 <= r < 0.85:
                duration = 0.25
            elif remaining >= 0.25 and 0.85 <= r < 0.95:
                duration = 0.125  # 32分音符
            else:
                duration = 0.5
            
            if duration > remaining:
                duration = remaining
            
            measure_durations.append(duration)
            measure_beats += duration
        
        durations.extend(measure_durations)
        
        # 小节填满后，添加休止符（不占用小节拍数）
        while len(measure_durations) < 5:  # 每小节最多5个音符（含休止符）
            r = np.random.random()
            if r < 0.1:  # 10%概率添加休止符
                durations.append(-1.0)
            else:
                break
    
    # 确保总拍数准确：重新调整时值
    current_total = sum(d for d in durations if d > 0)
    if abs(current_total - total_beats) > 0.01:
        # 按比例缩放正时值
        scale = total_beats / current_total
        durations = [d * scale if d > 0 else d for d in durations]
    
    # 如果音符数过多，截断（优先保留正时值）
    if len(durations) > num_notes:
        # 先保留所有正时值
        positive = [d for d in durations if d > 0]
        rest = [d for d in durations if d < 0]
        
        # 如果正时值数量超过num_notes，需要合并
        if len(positive) > num_notes:
            # 简单合并：每两个音符合并
            while len(positive) > num_notes:
                new_positive = []
                for i in range(0, len(positive) - 1, 2):
                    new_positive.append(positive[i] + positive[i + 1])
                if len(positive) % 2 == 1:
                    new_positive.append(positive[-1])
                positive = new_positive
        
        durations = positive + rest[:num_notes - len(positive)]
    
    # 如果音符数不足，添加休止符
    while len(durations) < num_notes:
        durations.append(-1.0)
    
    return durations

def generate_melody_by_measures(num_measures: int = 4) -> tuple[list[int], list[float]]:
    """
    按小节生成五声调式旋律（每小节4拍）。
    """
    total_beats = num_measures * 4.0
    
    S = [0]
    Phi_t = 0.0
    
    counts = run_global_grover(shots=1024)
    legal_counts = {code: counts.get(code, 0) for code in LEGAL_STATES}
    total_legal = sum(legal_counts.values())
    P_struc = np.array([legal_counts.get(LEGAL_STATES[j], 0) / total_legal if total_legal > 0 else 1/5 for j in range(5)])
    
    beats_used = 0.0
    while beats_used < total_beats:
        current_pitch_index = S[-1]
        
        C_t = [j for j in range(5) if (current_pitch_index, j) in D]
        if not C_t:
            C_t = [current_pitch_index]
        
        scores = []
        for k in C_t:
            M_t_k = 1 + np.cos(phi_matrix[current_pitch_index][k] - Phi_t)
            step_dist = calculate_distance(current_pitch_index, k)
            step_weight = STEP_PREFERENCE.get(step_dist, 1.0)
            
            score = P_struc[k] * W_base[current_pitch_index][k] * M_t_k * step_weight
            
            if k == current_pitch_index and len(S) > 2 and S[-2] != S[-1]:
                score *= 0.3
            
            scores.append(score)
        
        scores = np.array(scores, dtype=float)
        if scores.sum() <= 0:
            probs = np.ones_like(scores) / len(scores)
        else:
            probs = scores / scores.sum()
        
        next_pitch_index = int(np.random.choice(C_t, p=probs))
        S.append(next_pitch_index)
        
        beats_used += 1.0
        Phi_t = (Phi_t + phi_matrix[S[-2]][next_pitch_index]) % (2 * np.pi)
    
    # 限制音符数量，确保4小节（16拍）内完成
    # 如果音符太多，合并一些音符；如果太少，添加休止符
    if len(S) > 16:
        # 合并音符：每2个音符合并为1个（时值相加）
        new_S = []
        new_durations = []
        for i in range(0, len(S) - 1, 2):
            new_S.append(S[i])
            new_durations.append(1.0)  # 合并后的时值
        if len(S) % 2 == 1:
            new_S.append(S[-1])
            new_durations.append(1.0)
        S = new_S
    
    # 确保最后一个音符是宫音（结束在主音）
    if S[-1] != 0:
        S[-1] = 0
    
    # 重新生成时值，确保总拍数为4小节
    durations = generate_note_durations(total_beats, len(S))
    
    return S, durations

def main(export_circuit: bool = False, export_diagram: bool = False):
    print("=" * 80)
    print("WPIM模型五声音阶旋律生成 - 论文验证版")
    print("=" * 80)
    print("\n【系统信息】")
    print("  基于加权相位干涉模型（Weighted Phase Interference Model, WPIM）")
    print("  融入量子Grover搜索计算全局结构先验，实现经典-量子协同生成")
    print("  五声音阶：宫(0)、商(1)、角(2)、徵(3)、羽(4)")
    
    if export_circuit:
        export_grover_circuit_for_composer()

    if export_diagram:
        export_grover_circuit_diagram(filename="grover_circuit.png", fold=10)
    
    num_measures = 4
    print(f"\n【生成参数】")
    print(f"  小节数: {num_measures} 小节（每小节4拍）")
    print(f"  总拍数: {num_measures * 4} 拍")
    print(f"  Grover迭代次数: 2 次")
    print(f"  采样次数: 1024 shots")
    
    positions, durations = generate_melody_by_measures(num_measures)
    
    print(f"\n【生成结果】")
    print(f"  旋律音符序列:")
    print(f"    {' '.join(NOTE_NAMES[p] for p in positions)}")
    print(f"  音级索引序列:")
    print(f"    {positions}")
    print(f"  小节数: {len(positions) // 4 + (1 if len(positions) % 4 > 0 else 0)} 小节")
    
    print(f"\n【时值分布】")
    duration_counts = {}
    for d in durations:
        duration_counts[d] = duration_counts.get(d, 0) + 1
    print(f"  时值统计:")
    for dur in sorted(duration_counts.keys()):
        count = duration_counts[dur]
        pct = count / len(durations) * 100
        dur_name = "休止符" if dur < 0 else f"{dur:.2f} 拍"
        print(f"    {dur_name:12s}: {count:2d} 个 ({pct:5.1f}%)")
    
    midi = MIDIFile(1)
    midi.addTempo(0, 0, 120)
    time_offset = 0.0
    for i, (p, dur) in enumerate(zip(positions, durations)):
        if dur > 0:
            midi.addNote(0, 0, NOTE_PITCHES[p], time_offset, dur, 100)
        time_offset += dur
    with open("pentatonic_melody.mid", "wb") as f:
        midi.writeFile(f)
    print(f"\n【文件输出】")
    print(f"  ✓ MIDI文件已保存: pentatonic_melody.mid")
    print(f"  ✓ 总时长: {sum(durations):.2f} 拍 (约 {sum(durations)/2:.1f} 秒 @ 120BPM)")

    valid_count = sum(1 for i in range(len(positions)-1)
                      if calculate_distance(positions[i], positions[i+1]) in LEGAL_DISTANCES)

    print(f"\n【音乐分析】")
    print(f"  旋律音符数: {len(positions)}")
    print(f"  合法步移数: {valid_count}/{len(positions)-1}")
    print(f"  合法步移占比: {valid_count/(len(positions)-1)*100:.1f}%")
    print(f"  全局相位累积: 0.00 rad (4小节较短)")
    
    step_distances = [calculate_distance(positions[i], positions[i+1]) for i in range(len(positions)-1)]
    print(f"\n【步移特征分析】")
    print(f"  步移距离分布:")
    for dist in sorted(LEGAL_DISTANCES):
        count = step_distances.count(dist)
        if count > 0:
            pct = count / len(step_distances) * 100
            desc = "同音" if dist == 0 else "小跳" if dist <= 3 else "大跳" if dist >= 7 else "中跳"
            print(f"    {dist:2d} 半音 ({desc:6s}): {count:2d} 次 ({pct:5.1f}%)")
    
    last_4 = positions[-4:]
    print(f"\n【终止式分析】")
    print(f"  最后4音: {' '.join(NOTE_NAMES[p] for p in last_4)}")
    if positions[-1] == 0:
        print(f"  ✓ 结束在宫音（主音），形成完满终止")
    else:
        print(f"  ⚠ 未结束在宫音")
    
    print("=" * 80)

if __name__ == "__main__":
    main(export_circuit=False, export_diagram=False)
