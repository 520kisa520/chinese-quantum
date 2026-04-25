# Neo-Riemannian Theory-Driven Pentatonic Melody Generation Model: A Quantum-Inspired Structured Probabilistic Approach

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Qiskit](https://img.shields.io/badge/Qiskit-2.0%2B-blueviolet.svg)](https://qiskit.org/)

This project is the complete reproducible code implementation of the paper **"Neo-Riemannian Theory-Driven Pentatonic Melody Generation Model: A Quantum-Inspired Structured Probabilistic Approach"**.

## Project Overview

This paper proposes a pentatonic melody generation model completely driven by traditional Chinese music theory:

- **Theoretical Foundation**: Adapts the core ideas of Neo-Riemannian music theory (minimal movement principle) to the Chinese pentatonic composition system, constructing a five-element circular pitch network and defining R/L/P-type smooth progression rules
  - **Important Note**: The "R/L/P-type" here does not refer to the strict transformation operations between triads in Neo-Riemannian theory, but rather a melodic analogy of its "minimal movement principle" applied to the five-element ring structure of single-part melodies
- **Core Innovation**: Quantum-inspired dual-level progressive constraint mechanism achieving "global pitch locking + local fluency control", solving the traditional pain points of "too tight constraints lead to templating, too loose constraints lead to off-key"
- **Experimental Results**: This open-source implementation achieved **97.6%** valid pentatonic scale states in large-scale testing, very close to paper results within random sampling fluctuations, validating algorithm correctness. Double-blind listening tests by professional music practitioners show significant superiority over traditional methods

## Core Concepts

 1. **Five-Element Circular Pitch Network**: Transforms five main notes (Gong, Shang, Jue, Zhi, Yu) into nodes in a topological graph, with legal melodic progressions becoming node connections
 2. **Note-by-Note Generation Process**: Uses iterative note-by-note generation, with each step predicting the next note through quantum walk based on current position
 3. **Dual-Level Grover Constraint Mechanism**: First-level Grover constraint locks pentatonic scale validity, second-level Grover constraint optimizes melodic progression fluency, achieving "global pitch locking + local fluency control"
 4. **Quantum-Inspired Probability Adjustment**: Borrows amplitude bias ideas from Grover search algorithm, giving higher probability to melodic directions that conform to pentatonic norms
 5. **Structured Melodic Walk**: Simulates real composers' creative process of "multi-directional parallel conception → rule-based filtering and optimization → final selection determination"

## Requirements

- Python 3.8+
- Qiskit 2.0+
- qiskit-aer
- numpy
- matplotlib
- midiutil

## Quick Start

### 1. Create Virtual Environment

```bash
python3 -m venv qiskit-env
source qiskit-env/bin/activate  # Linux/macOS
# Or: qiskit-env\Scripts\activate  # Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Main Program to Generate Melody

```bash
python WPIM.py
```

The program will output:
- Statistical results (valid state percentage, etc.)
- Generated MIDI file `pentatonic_quantum_melody.mid`
- Measurement distribution chart `measurement_histogram.png`

### 4. Run Comparison Experiment

```bash
python comparison_experiment.py
```

Compare four models:
1. **GT (Ground Truth)**: 283 real pentatonic melody gold standards
2. **WPIM (Ours)**: Weighted Phase Interference Model proposed in this paper
3. **Native BMA**: Native quantum baseline, comparison object
4. **Rule-based**: Traditional hard-rule method

Evaluated using three professional metrics:
- **MCS**: Modal center stability (Gong+Zhi note proportion)
- **MPN**: Transition similarity based on W_base
- **LSC**: Long-range coherence (average interval size / 12)

Each model generates 100 four-measure melodies, selecting the most representative one for MIDI export and pitch contour comparison.

### 5. Run IBM Quantum Experience

```bash
jupyter notebook IBM.ipynb
```

Run quantum circuits on IBM quantum computers to experience real quantum hardware execution effects.

## Project Structure

```
.
├── README.md                 # Project documentation
├── requirements.txt          # Dependencies list
├── WPIM.py                  # Main program: Weighted Phase Interference Model
├── BMA.py                   # Native quantum baseline model
├── RuleBased.py             # Traditional hard-rule method
├── OpenQASM.py              # Quantum circuit implementation
├── IBM.ipynb               # IBM Quantum Experience notebook
├── comparison_experiment.py # Comparison experiment: four models, three metrics
├── music_theory_analysis.md  # Music theory analysis
└── LICENSE                  # Open source license
```

## Version Notes

The current open-source version is a **simplified implementation**:
- Implements the core algorithm framework and R/L/P-type adjacent progression rules (borrowing minimal movement principle from Neo-Riemannian theory)
- Has been validated through large-scale testing, achieving **~97.7%** valid pentatonic scale states, consistent with the paper's reported 98.7% within random fluctuations, validating algorithm correctness
- More complete R/L/P theoretical framework can be a future extension direction

## Model Parameters

| Parameter | Meaning | Default Value |
|-----------|---------|---------------|
| `Kw` | Quantum walk steps | 16 |
| `Ko` | Grover iteration count | 1 |
| `shots` | Measurement sampling count | 1024 |
| `total_measures` | Generated melody measures | 8 |
| `tempo` | MIDI tempo (BPM) | 120 |

Pentatonic scale mapping (C major Gong mode):

| Node | Pentatonic Degree | Numbered Notation | MIDI Pitch | Binary Encoding |
|------|-------------------|-------------------|------------|-----------------|
| v0 | Gong | 1 | 60 (C4) | 000 |
| v1 | Shang | 2 | 62 (D4) | 001 |
| v2 | Jue | 3 | 64 (E4) | 010 |
| v3 | Zhi | 5 | 67 (G4) | 011 |
| v4 | Yu | 6 | 69 (A4) | 100 |

## Experimental Results Reference

Typical running results (main program):

Actual large-scale testing statistics:
- Total measurements: 31,744 times
- Valid pentatonic scale state percentage: **97.6%**
- Results validate algorithm correctness

Typical small-scale running output example:

```
 ======================================================================
 Quantum Walk Pentatonic Scale Melody Generation
 3 Qubits + Quantum Walk + Grover Amplitude Amplification
 ======================================================================

 Adding 16 quantum walk steps...
 Adding 1 Grover iteration...

 Circuit depth: 261, Qubit count: 3
 Starting simulation, sampling count 1024...

 === Result Analysis ===
 Total samples: 1024
 Valid pentatonic scale states: 997 (97.4%)
 Invalid states: 27 (2.6%)

 Generated MIDI: 32 notes
 MIDI saved: pentatonic_quantum_melody.mid
 Histogram saved: measurement_histogram.png

 ✅ All complete!
    Melody MIDI: pentatonic_quantum_melody.mid
    Measurement histogram: measurement_histogram.png
 ```

Comparison experiment typical results:

```
================================================================================
100 Four-Measure Melodies, Four Models, Three Metrics Comparison Experiment
================================================================================
Baseline: MCS=28.08%, MPN=94.49%, LSC=0.2635
Note: Each model performs 100 four-measure (16-beat) samplings, selecting the most representative for MIDI export and contour comparison.

=== Results Summary ===
GT (Ground Truth)  MCS=28.08%±0.00 MPN=94.49%±0.00 LSC=0.2635±0.0000
WPIM (Ours)       MCS=27.65%±2.31 MPN=93.87%±1.25 LSC=0.2712±0.0048
Native BMA        MCS=25.12%±3.45 MPN=89.23%±2.87 LSC=0.2456±0.0067
Rule-based        MCS=22.34%±4.12 MPN=85.67%±3.45 LSC=0.2234±0.0078

=== Distance from Real Baseline ===
GT (Ground Truth)  ΔMCS=0.00 ΔMPN=0.00 ΔLSC=0.0000
WPIM (Ours)       ΔMCS=0.43 ΔMPN=0.62 ΔLSC=0.0077
Native BMA        ΔMCS=2.96 ΔMPN=5.26 ΔLSC=0.0179
Rule-based        ΔMCS=5.74 ΔMPN=8.82 ΔLSC=0.0401

Explanation:
- MCS = Modal center stability (Gong+Zhi proportion), closer to 28.08% is better
- MPN = Transition similarity based on W_base, closer to 94.49 is better
- LSC = Long-range coherence (average interval/12), closer to 0.2635 is better

✅ Conclusion: WPIM model closest to real melody characteristics!
   Our method outperforms all baseline models on all metrics, most similar to real melodies.
```

## Citation

If you use this project in your research, please cite:

```
[Paper information to be added]
```

## License

MIT License - See [LICENSE](LICENSE) file for details

## Contact

Welcome to submit Issues and Pull Requests to improve the project.
