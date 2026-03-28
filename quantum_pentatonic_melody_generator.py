# Last updated in English
#!/usr/bin/env python3
"""
Quantum-Inspired Pentatonic Melody Generation - Paper Verified Version

Strategy: Amplify 5 legal pentatonic states using Grover's algorithm,
then apply high weight to valid transitions
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np
from midiutil import MIDIFile

LEGAL_STATES = ["000", "001", "010", "011", "100"]
NOTE_NAMES = ["Gong", "Shang", "Jue", "Zhi", "Yu"]
NOTE_PITCHES = [60, 62, 64, 67, 69]
KO = 2
BOOST = 100.0


def add_phase_flip(qc, code):
    """Add phase flip to target state"""
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


def run_global_grover(shots=1024):
    qc = QuantumCircuit(3, 3)
    qc.h([0, 1, 2])
    qc.barrier()
    for _ in range(KO):
        qc = grover_oracle(qc, LEGAL_STATES)
        qc = grover_diffusion(qc)
    qc.measure([0, 1, 2], [0, 1, 2])
    return AerSimulator().run(qc, shots=shots).result().get_counts()


def main():
    print("=" * 70)
    print("Quantum-Inspired Pentatonic Melody Generation - Paper Verified")
    print("=" * 70)

    counts = run_global_grover(shots=1024)

    total = sum(counts.values())
    legal = sum(counts.get(s, 0) for s in LEGAL_STATES)
    legal_ratio = legal / total * 100

    legal_counts = {code: counts.get(code, 0) for code in LEGAL_STATES}

    positions = [0]

    for _ in range(31):
        current = positions[-1]
        valid = [(current + 1) % 5, (current - 1) % 5]

        probs = [legal_counts.get(LEGAL_STATES[p], 0) for p in range(5)]

        for p in valid:
            probs[p] *= BOOST

        total_prob = sum(probs)
        if total_prob > 0:
            probs = [x / total_prob for x in probs]

        next_pos = np.random.choice(5, p=probs)
        positions.append(next_pos)

    print(f"\nGenerated melody: {' '.join(NOTE_NAMES[p] for p in positions)}")

    midi = MIDIFile(1)
    midi.addTempo(0, 0, 120)
    for i, p in enumerate(positions):
        midi.addNote(0, 0, NOTE_PITCHES[p], i, 1, 100)
    with open("pentatonic_melody.mid", "wb") as f:
        midi.writeFile(f)
    print("✓ MIDI saved: pentatonic_melody.mid")

    valid_count = sum(1 for i in range(len(positions)-1)
                      if (positions[i+1] - positions[i]) % 5 in [1, 4])

    print("\nStatistics:")
    print(f"  Grover measurement: {legal}/{total} = {legal_ratio:.1f}%")
    print(f"  Melody length: {len(positions)} notes")
    print(
        f"  P/E/F smooth transitions: {valid_count}/{len(positions)-1} = {valid_count/(len(positions)-1)*100:.1f}%")
    print("=" * 70)


if __name__ == "__main__":
    main()
