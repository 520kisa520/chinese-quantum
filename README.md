# Quantum-Inspired Pentatonic Melody Generation - Documentation

This file contains comprehensive documentation for the quantum-inspired pentatonic melody generation project, placed parallel to the LICENSE file as requested.

## Project Overview

This project implements a novel approach to generating pentatonic melodies using quantum computing principles and Neo-Riemannian music theory adapted for traditional Chinese music.

## Key Features

- **Quantum-Inspired Algorithm**: Uses quantum walk and Grover's algorithm for melody generation
- **Neo-Riemannian Theory Adaptation**: Adapts Western music theory concepts to Chinese pentatonic scales
- **High Validity Rate**: Achieves 97.6% valid pentatonic scale states
- **Dual-Language Support**: Available in both Chinese and English versions

## Directory Structure

```
chinese quantum/
├── LICENSE                    # MIT License
├── README.md                  # Project documentation
├── chinese_version/           # Chinese implementation
│   ├── README.md             # Chinese documentation
│   ├── WPIM.py               # Weighted Phase Interference Model
│   ├── BMA.py                # Native quantum baseline model
│   ├── RuleBased.py          # Traditional hard-rule method
│   ├── OpenQASM.py           # Quantum circuit implementation
│   ├── IBM.ipynb             # IBM Quantum Experience notebook
│   ├── comparison_experiment.py  # Four models, three metrics comparison
│   ├── music_theory_analysis.md  # Music theory analysis
│   ├── example_outputs/      # Sample results
│   └── requirements.txt      # Dependencies
└── english_version/          # English implementation
    ├── README.md             # English documentation
    ├── WPIM.py               # Weighted Phase Interference Model
    ├── BMA.py                # Native quantum baseline model
    ├── RuleBased.py          # Traditional hard-rule method
    ├── OpenQASM.py           # Quantum circuit implementation
    ├── IBM.ipynb             # IBM Quantum Experience notebook
    ├── comparison_experiment.py  # Four models, three metrics comparison
    ├── music_theory_analysis.md  # Music theory analysis
    ├── example_outputs/      # Sample results
    └── requirements.txt      # Dependencies
```

## Core Components

### 1. WPIM.py (Weighted Pitch Interaction Model)
- Main melody generation algorithm
- Implements quantum walk with Grover constraints
- Dual-level constraint mechanism for pitch validity and fluency

### 2. BMA.py (Native Quantum Baseline)
- Native quantum baseline model
- Uses quantum amplitude amplification (BMA) algorithm
- Baseline for quantum approach comparison

### 3. RuleBased.py
- Traditional hard-rule melody generation
- Classical approach comparison
- Uses pentatonic legal step movement rules

### 4. OpenQASM.py
- Quantum circuit implementation
- OpenQASM code for quantum hardware execution

### 5. IBM.ipynb
- Jupyter notebook for IBM Quantum Experience
- Interactive quantum circuit testing

## Algorithm Details

### Quantum Walk Process
1. Initialize quantum state with pentatonic scale notes
2. Apply quantum walk operators for note transitions
3. Use Grover's algorithm for amplitude amplification
4. Measure to obtain melody sequence

### Dual-Level Constraints
- **Level 1**: Ensures pentatonic scale validity
- **Level 2**: Optimizes melodic fluency and smoothness

### Neo-Riemannian Adaptation
- Adapts R/L/P operations for pentatonic scales
- Implements minimal movement principle
- Creates five-element circular pitch network

## Installation and Usage

### Prerequisites
- Python 3.8+
- Qiskit 2.0+
- IBM Quantum account (for hardware execution)

### Setup
```bash
# Clone repository
git clone [repository-url]
cd "chinese quantum"

# Choose language version
cd chinese_version  # or english_version

# Create virtual environment
python3 -m venv qiskit-env
source qiskit-env/bin/activate  # Linux/macOS
# or qiskit-env\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### Running the Code
```bash
# Main melody generation
python WPIM.py

# Four models, three metrics comparison experiment
python comparison_experiment.py

# Individual algorithms
python BMA.py
python RuleBased.py

# IBM Quantum Experience
jupyter notebook IBM.ipynb
```

## Experimental Results

### Performance Metrics
- **Valid Pentatonic States**: 97.6%
- **Circuit Depth**: 261 gates
- **Qubit Count**: 3 qubits
- **Sampling Shots**: 1024

### Four Models Comparison Experiment
- **GT (Ground Truth)**: 283 real pentatonic melody baselines
- **WPIM (Ours)**: Weighted Phase Interference Model, closest to real melodies
- **Native BMA**: Native quantum baseline model
- **Rule-based**: Traditional hard-rule method

### Evaluation Metrics
- **MCS**: Modal center stability (Gong+Zhi note proportion)
- **MPN**: Transition similarity based on W_base
- **LSC**: Long-range coherence (average interval size / 12)

### Experimental Design
- **Sample Size**: 100 four-measure melodies per model
- **Ground Truth**: 283 real pentatonic melodies from professional composers
- **Selection Method**: Choose most representative sequence for each model
- **Output**: MIDI files and pitch contour comparison charts
- **Baseline Values**: MCS=28.08%, MPN=94.49%, LSC=0.2635 (from real melodies)

## Music Theory Integration

### Pentatonic Scale Mapping
| Node | Note | Numbered Notation | MIDI Pitch | Binary |
|------|------|-------------------|------------|--------|
| v0 | Gong (宫) | 1 | 60 (C4) | 000 |
| v1 | Shang (商) | 2 | 62 (D4) | 001 |
| v2 | Jiao (角) | 3 | 64 (E4) | 010 |
| v3 | Zhi (徵) | 5 | 67 (G4) | 011 |
| v4 | Yu (羽) | 6 | 69 (A4) | 100 |

### Neo-Riemannian Operations
- **R-type**: Relative transformations
- **L-type**: Leading-tone transformations  
- **P-type**: Parallel transformations

## Output Files

### Generated Files
- `pentatonic_quantum_melody.mid` - Generated melody
- `measurement_histogram.png` - Probability distribution
- `comparison_results.txt` - Experimental results

### Analysis Files
- `music_theory_analysis.md` - Detailed music theory
- `example_outputs/` - Sample results

## Future Development

### Planned Features
- Extended R/L/P theoretical framework
- Multi-scale support beyond pentatonic
- Real-time quantum hardware integration
- GUI interface for melody generation

### Research Directions
- Quantum advantage in music composition
- Cross-cultural music theory integration
- AI-assisted music generation

## Contributing

### Guidelines
1. Fork the repository
2. Create feature branch
3. Implement changes with tests
4. Submit pull request

### Code Style
- Follow PEP 8 guidelines
- Include docstrings for functions
- Add comments for quantum operations

## References

### Academic Papers
- [Paper information to be added]

### Quantum Computing
- Qiskit Documentation: https://qiskit.org/
- IBM Quantum Experience: https://quantum-computing.ibm.com/

### Music Theory
- Neo-Riemannian Theory literature
- Chinese pentatonic scale research

## Support

### Issues and Questions
- GitHub Issues: Report bugs and feature requests
- Documentation: Check this file and READMEs
- Examples: See `example_outputs/` directory

### Contact
- [Contact information to be added]

---

*This documentation is maintained alongside the LICENSE file to provide comprehensive project information.*
