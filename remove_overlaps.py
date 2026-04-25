#!/usr/bin/env python3
"""
删除283-Wbase目录中MIDI文件的叠音（同时开始的音符）
只删除叠音，不调整音高
"""

import pretty_midi
import os

def remove_overlaps(filename):
    """删除MIDI文件中的叠音"""
    try:
        pm = pretty_midi.PrettyMIDI(filename)
        
        # 获取所有音符
        all_notes = []
        for inst in pm.instruments:
            for note in inst.notes:
                all_notes.append((note.start, note.pitch, note.duration, note))
        
        # 按开始时间排序
        all_notes.sort()
        
        # 检查叠音
        notes_to_remove = []
        for i in range(len(all_notes)-1):
            if all_notes[i][0] == all_notes[i+1][0]:  # 相同开始时间
                # 保留第一个，删除后面的
                notes_to_remove.append(all_notes[i+1][3])
        
        # 删除叠音
        removed_count = 0
        for inst in pm.instruments:
            original_count = len(inst.notes)
            inst.notes = [note for note in inst.notes if note not in notes_to_remove]
            removed_count = original_count - len(inst.notes)
        
        if removed_count > 0:
            # 保存修复后的文件
            pm.write(filename)
            return True, removed_count
        else:
            return False, 0
            
    except Exception as e:
        print(f"处理 {filename} 时出错: {e}")
        return False, 0

def main():
    """处理283-Wbase目录中的所有MIDI文件"""
    import glob
    
    midi_files = glob.glob('283-Wbase/*.mid')
    print(f'找到 {len(midi_files)} 个MIDI文件')
    
    fixed_count = 0
    total_removed = 0
    
    for filename in midi_files:
        fixed, removed = remove_overlaps(filename)
        if fixed:
            fixed_count += 1
            total_removed += removed
            print(f'{filename}: 删除了 {removed} 个叠音')
    
    print(f'\n完成！')
    print(f'修复了 {fixed_count} 个文件')
    print(f'总共删除了 {total_removed} 个叠音')

if __name__ == '__main__':
    main()
