#!/usr/bin/env python3
"""
对照实验：100 次生成 4 小节旋律。将四模型、三指标对比，多次采样后选最典型一条进行输出midi与作图进行比较。

模型：
1. GT（Ground Truth）：283 个真实五声旋律金标准
2. WPIM（Ours）：本文提出的加权相位干涉模型
3. Native BMA：原生量子基线，对比对象
4. Rule-based：传统硬规则方法

指标：
- MCS: 调式重心稳定度
- MPN: 基于 W_base 的过渡相似度
- LSC: 长程连贯度（平均音程大小 / 12）
"""

import os
import sys
import random
import numpy as np
import pretty_midi
import matplotlib.pyplot as plt
from midiutil import MIDIFile

# Ensure local package imports resolve when running this script from the repository root or the chinese_version folder.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from chinese_version.WPIM import generate_melody_by_measures, W_base, NOTE_PITCHES, generate_note_durations
from chinese_version.BMA import generate_native_bma_melody
from chinese_version.RuleBased import generate_rule_based_melody


def generate_wpim_melody(length=16):
    """WPIM 生成4小节旋律（带时值信息）"""
    melody, durations = generate_melody_by_measures(num_measures=4)
    return melody, durations


def generate_native_bma_melody_with_durations(length=16):
    """Native BMA 生成4小节旋律（带时值信息）"""
    melody = generate_native_bma_melody(length=length)
    durations = generate_note_durations(total_beats=4.0 * 4.0, num_notes=len(melody))
    return melody, durations


def generate_rule_based_melody_with_durations(length=16):
    """Rule-based 生成4小节旋律（带时值信息）"""
    melody = generate_rule_based_melody(length=length)
    durations = generate_note_durations(total_beats=4.0 * 4.0, num_notes=len(melody))
    return melody, durations

NOTE_NAMES = ["Gong", "Shang", "Jue", "Zhi", "Yu"]
NOTE_PITCHES_ARRAY = np.array(NOTE_PITCHES)
LEGAL_DISTANCES = {0, 2, 3, 4, 5, 7, 9}
D = {(i, j) for i in range(5) for j in range(5) if abs(NOTE_PITCHES_ARRAY[i] - NOTE_PITCHES_ARRAY[j]) in LEGAL_DISTANCES}
LEGAL_STATES = ["000", "001", "010", "011", "100"]
GT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '283-Wbase'))

BASELINE = {"MCS": 28.08, "MPN": 94.49, "LSC": 0.2635}

random.seed(1234)
np.random.seed(1234)


def calculate_distance(i, j):
    """计算音级i到j的半音距离（与WPIM.py保持一致）"""
    p_i = NOTE_PITCHES_ARRAY[i]
    p_j = NOTE_PITCHES_ARRAY[j]
    return min(abs(p_i - p_j), 12 - abs(p_i - p_j))


def score_mcs(sequence):
    """计算调式重心稳定度：宫音(0)和徵音(3)占总音数比例"""
    if len(sequence) == 0:
        return 0.0
    gong_zhi_count = sum(1 for note in sequence if note in [0, 3])
    return gong_zhi_count / len(sequence) * 100.0


def score_mpn(sequence):
    if len(sequence) < 2:
        return 100.0
    values = []
    for a, b in zip(sequence, sequence[1:]):
        row = W_base[a]
        if row.max() == row.min():
            values.append(0.0)
            continue
        normalized = (row[b] - row.min()) / (row.max() - row.min())
        values.append(normalized)
    return float(np.mean(values) * 100.0)


def score_lsc(sequence):
    if len(sequence) < 2:
        return 0.0
    intervals = [calculate_distance(a, b) for a, b in zip(sequence, sequence[1:])]
    return float(np.mean(intervals) / 12.0)


def evaluate_sequence(sequence):
    return {
        "MCS": score_mcs(sequence),
        "MPN": score_mpn(sequence),
        "LSC": score_lsc(sequence),
    }


def load_ground_truth_sequences(root=None):
    if root is None:
        root = GT_ROOT
    sequences = []
    for filename in sorted(os.listdir(root)):
        if not filename.lower().endswith(('.mid', '.midi')):
            continue
        path = os.path.join(root, filename)
        try:
            pm = pretty_midi.PrettyMIDI(path)
        except:
            continue
        notes = []
        for inst in pm.instruments:
            for note in inst.notes:
                notes.append((note.start, note.pitch, note.duration))
        notes.sort(key=lambda x: x[0])
        
        # 按4小节（16拍）切分
        if len(notes) < 16:
            continue
        
        # 只取前16个音符（4小节）
        notes = notes[:16]
        
        sequence = []
        durations = []
        valid = True
        for start, pitch, duration in notes:
            if pitch in NOTE_PITCHES:
                sequence.append(NOTE_PITCHES.index(pitch))
                durations.append(duration)
            else:
                valid = False
                break
        
        if valid and len(sequence) == 16:
            # 调整时值，确保总拍数为4小节（16拍）
            current_total = sum(d for d in durations if d > 0)
            if abs(current_total - 16.0) > 0.01:
                scale = 16.0 / current_total
                durations = [d * scale for d in durations]
            sequences.append((sequence, durations))
    if not sequences:
        raise RuntimeError(f"无法加载 GT 曲目：{root} 中未找到有效五声 MIDI 文件")
    return sequences


def sample_ground_truth_sequences(count=100):
    sequences = load_ground_truth_sequences()
    if len(sequences) >= count:
        return random.sample(sequences, count)
    return sequences


def choose_representative_sequence(sequences):
    histograms = np.array([np.bincount(seq, minlength=5) / len(seq) for seq in sequences])
    avg_hist = np.mean(histograms, axis=0)
    best_index = int(np.argmin(np.sum(np.abs(histograms - avg_hist), axis=1)))
    return sequences[best_index]


def evaluate_ground_truth(count=100):
    sequences = sample_ground_truth_sequences(count)
    return aggregate_results([evaluate_sequence(seq) for seq in sequences])


def generate_model_samples(generator, count=100, length=16, **kwargs):
    """生成模型样本，支持返回 (sequence, durations) 或仅 sequence"""
    sequences = []
    all_durations = []
    for _ in range(count):
        result = generator(length=length, **kwargs)
        if isinstance(result, tuple):
            seq, durations = result
            # 确保总拍数为4小节（16拍）
            # 重新分配时值，确保每小节4拍
            total = sum(d for d in durations if d > 0)
            if abs(total - 16.0) > 0.01:
                # 按比例缩放正时值，确保总拍数为16
                scale = 16.0 / total
                durations = [d * scale if d > 0 else d for d in durations]
            sequences.append(seq)
            all_durations.append(durations)
        else:
            sequences.append(result)
            all_durations.append(None)
    
    metrics = [evaluate_sequence(seq) for seq in sequences]
    summary = aggregate_results(metrics)
    representative_seq = choose_representative_sequence(sequences)
    # 找到代表序列的索引
    representative_idx = sequences.index(representative_seq)
    representative_durations = all_durations[representative_idx]
    return summary, representative_seq, representative_durations


def format_melody_example(sequence):
    groups = [" ".join(str(x) for x in sequence[i:i+4]) for i in range(0, len(sequence), 4)]
    return " | ".join(groups)


def export_midi(filename, sequence, durations=None):
    """导出MIDI文件，支持时值和休止符"""
    midi = MIDIFile(1)
    midi.addTempo(0, 0, 120)
    
    time_offset = 0.0
    for i, p in enumerate(sequence):
        dur = durations[i] if durations is not None else 1.0
        # 休止符用负值表示，不添加音符
        if dur > 0:
            midi.addNote(0, 0, NOTE_PITCHES[p], time_offset, dur, 100)
        time_offset += dur
    
    with open(filename, "wb") as f:
        midi.writeFile(f)
    return filename


def plot_pitch_contours(sequences, labels, filename="pitch_contours.png"):
    plt.figure(figsize=(10, 4))
    for seq, label in zip(sequences, labels):
        plt.plot(range(len(seq)), seq, marker='o', markersize=4, label=label)
    plt.yticks(range(5), NOTE_NAMES)
    plt.xlabel("Note position")
    plt.ylabel("Pitch degree")
    plt.title("Pitch contour comparison of 32-note melodies")
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc="upper left")
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()
    return filename


def save_example_outputs(results, output_dir="example_outputs"):
    os.makedirs(output_dir, exist_ok=True)
    print("\n=== 示例旋律文本 ===")
    examples = []
    for name, item in results.items():
        if name == "GT (Ground Truth)":
            seq = item["example"]
            durs = item["durations"]
        else:
            seq = item["example"]
            durs = item["durations"]
        examples.append((name, seq, durs))
        print(f"{name}: {format_melody_example(seq)}")

    print("\n=== 导出 MIDI 示例 ===")
    midi_files = []
    for name, seq, durs in examples:
        filename = os.path.join(output_dir, f"{name.replace(' ', '_').replace('(', '').replace(')', '')}_example.mid")
        export_midi(filename, seq, durations=durs)
        midi_files.append(filename)
        print(f"已导出：{filename}")

    contour_file = os.path.join(output_dir, "pitch_contour_comparison.png")
    plot_pitch_contours([seq for _, seq, _ in examples], [name for name, _, _ in examples], filename=contour_file)
    print(f"已生成音高轮廓图：{contour_file}")
    return midi_files, contour_file


def aggregate_results(metrics_list):
    summary = {}
    for metric in ["MCS", "MPN", "LSC"]:
        values = [item[metric] for item in metrics_list]
        summary[metric] = {
            "mean": float(np.mean(values)),
            "std": float(np.std(values, ddof=1)) if len(values) > 1 else 0.0,
            "min": float(np.min(values)),
            "max": float(np.max(values)),
        }
    return summary


def run_model_experiment(generator, count=100, length=32, **kwargs):
    metrics_list = []
    for _ in range(count):
        seq = generator(length=length, **kwargs)
        metrics_list.append(evaluate_sequence(seq))
    return aggregate_results(metrics_list)


def format_summary(name, stats):
    return (
        f"{name:<12} "
        f"MCS={stats['MCS']['mean']:.2f}%±{stats['MCS']['std']:.2f} "
        f"MPN={stats['MPN']['mean']:.2f}%±{stats['MPN']['std']:.2f} "
        f"LSC={stats['LSC']['mean']:.4f}±{stats['LSC']['std']:.4f}"
    )


def main():
    print("=" * 88)
    print("100 首 4 小节旋律、四模型、三指标对比实验")
    print("=" * 88)
    print("基准：MCS=28.08%，MPN=94.49%，LSC=0.2635")
    print("说明：每个模型均进行 100 次 4 小节（16拍）采样，选取最典型一条用于 MIDI 导出与轮廓比较。\n")

    results = {}
    print("正在运行：GT (Ground Truth)")
    gt_data = sample_ground_truth_sequences(100)
    gt_sequences = [seq for seq, _ in gt_data]
    gt_durations = [durs for _, durs in gt_data]
    results["GT (Ground Truth)"] = {
        "summary": aggregate_results([evaluate_sequence(seq) for seq in gt_sequences]),
        "example": choose_representative_sequence(gt_sequences),
        "durations": gt_durations[gt_sequences.index(choose_representative_sequence(gt_sequences))],
    }

    models = [
        ("WPIM (Ours)", generate_wpim_melody, {}),
        ("Native BMA", generate_native_bma_melody_with_durations, {}),
        ("Rule-based", generate_rule_based_melody_with_durations, {}),
    ]

    for name, generator, kwargs in models:
        print(f"正在运行：{name}")
        summary, representative, representative_durations = generate_model_samples(generator, count=100, **kwargs)
        results[name] = {
            "summary": summary,
            "example": representative,
            "durations": representative_durations,
        }

    print("\n=== 结果汇总 ===")
    for name, item in results.items():
        print(format_summary(name, item["summary"]))

    print("\n=== 与真实基准距离 ===")
    for name, item in results.items():
        stats = item["summary"]
        diff = {
            metric: abs(stats[metric]["mean"] - BASELINE[metric])
            for metric in BASELINE
        }
        print(
            f"{name:<12} "
            f"ΔMCS={diff['MCS']:.2f} "
            f"ΔMPN={diff['MPN']:.2f} "
            f"ΔLSC={diff['LSC']:.4f}"
        )

    save_example_outputs(results)

    print("\n说明：")
    print("- MCS = 调式重心稳定度(宫音+徵音占比)，越接近 28.08% 越好")
    print("- MPN = 基于 W_base 的过渡相似度，越接近 94.49 越好")
    print("- LSC = 长程连贯度(平均音程/12)，越接近 0.2635 越好")


if __name__ == '__main__':
    main()
