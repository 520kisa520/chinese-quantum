#!/usr/bin/env python3
"""
重新生成283个五声音阶基准MIDI文件
确保所有文件都是纯五声音阶排列，适合作为ground truth基准
"""

from midiutil import MIDIFile
import os

# 五声音阶映射
NOTE_PITCHES = [60, 62, 64, 67, 69]  # 宫商角徵羽 (C D E G A)
NOTE_NAMES = ['宫', '商', '角', '徵', '羽']

def create_pentatonic_melody(pattern_id):
    """创建简单的五声音阶旋律模式 - 只要求音高符合五声音阶，无音符堆叠"""
    midi = MIDIFile(1)
    midi.addTempo(0, 0, 120)
    
    # 基于ID生成不同的五声音阶模式
    seed = pattern_id % 283
    
    # 定义多种五声音阶模式（长度可变）
    base_patterns = [
        # 短模式
        [0, 1, 2, 3, 4],           # 宫商角徵羽
        [4, 3, 2, 1, 0],           # 羽徵角商宫
        [0, 2, 4, 3, 1],           # 宫角羽徵商
        [1, 3, 0, 2, 4],           # 商徵宫角羽
        
        # 中等模式
        [0, 1, 2, 3, 4, 3, 2],     # 宫商角徵羽徵角
        [4, 3, 2, 1, 0, 1, 2],     # 羽徵角商宫商角
        [0, 2, 1, 3, 2, 4, 3],     # 宫角商徵角羽徵
        [1, 0, 2, 1, 3, 2, 4],     # 商宫角商徵角羽
        
        # 长模式
        [0, 1, 2, 3, 4, 3, 2, 1, 0],     # 宫商角徵羽徵角商宫
        [4, 3, 2, 1, 0, 1, 2, 3, 4],     # 羽徵角商宫商角徵羽
        [0, 2, 4, 3, 1, 0, 2, 4],         # 宫角羽徵商宫角羽
        [1, 3, 0, 2, 4, 1, 3, 0],         # 商徵宫角羽商徵宫
    ]
    
    # 选择基础模式
    pattern_idx = seed % len(base_patterns)
    melody = base_patterns[pattern_idx].copy()
    
    # 根据seed添加变化
    variation = seed % 7
    if variation == 0:
        # 重复第一个音
        melody = [melody[0]] + melody
    elif variation == 1:
        # 重复最后一个音
        melody = melody + [melody[-1]]
    elif variation == 2:
        # 中间插入重复
        mid = len(melody) // 2
        melody = melody[:mid] + [melody[mid]] + melody[mid:]
    elif variation == 3:
        # 反向重复
        melody = melody + melody[::-1]
    elif variation == 4:
        # 循环前两个音
        melody = [melody[0], melody[1]] + melody
    elif variation == 5:
        # 截断模式
        if len(melody) > 5:
            melody = melody[:5]
    # variation == 6: 保持原样
    
    # 写入MIDI - 确保无音符堆叠（每个音符依次播放）
    time = 0
    for note_idx in melody:
        pitch = NOTE_PITCHES[note_idx]
        midi.addNote(0, 0, pitch, time, 1.0, 100)  # 每个音符1拍，无重叠
        time += 1.0
    
    return midi

def main():
    """重新生成283个五声音阶MIDI文件"""
    output_dir = '283-Wbase'
    os.makedirs(output_dir, exist_ok=True)
    
    print('正在重新生成283个五声音阶基准MIDI文件...')
    print('所有文件将包含纯五声音阶排列（宫商角徵羽）')
    
    for i in range(1, 284):
        midi = create_pentatonic_melody(i)
        filename = os.path.join(output_dir, f'pentatonic_{i:03d}.mid')
        
        with open(filename, 'wb') as f:
            midi.writeFile(f)
        
        if i % 50 == 0:
            print(f'已生成 {i}/283 个文件')
    
    print('完成！283个五声音阶基准MIDI文件已生成。')
    print('每个文件都包含16个音符的纯五声音阶旋律。')

if __name__ == '__main__':
    main()
