# Quantum Error Correction Simulation

A beginner-friendly implementation of quantum error correction using **repetition codes** to protect against bit-flip noise. This project uses [Stim](https://github.com/quantumlib/Stim) and Python to simulate quantum circuits and demonstrate how error correction can reduce logical error rates.

## 🎯 Project Overview

This project demonstrates:
- ✅ Implementation of **repetition codes** (3-qubit, 5-qubit, 7-qubit)
- ✅ Simulation of **Bit-Flip (X)** and **Phase-Flip (Z)** noise
- ✅ Comparison of **protected vs unprotected** qubits
- ✅ Analysis of how **code size** affects error correction performance
- ✅ Study of **measurement error** impact on quantum error correction

## 📚 Background: Quantum Error Correction

### Why Error Correction?

Quantum computers are extremely sensitive to noise. Even small environmental disturbances can cause errors in quantum computations. Unlike classical bits, quantum bits (qubits) cannot be simply copied due to the **no-cloning theorem**. Quantum error correction solves this by encoding logical qubits into multiple physical qubits.

### Repetition Codes

The **repetition code** is the simplest quantum error correction code. It protects against bit-flip errors (X errors) by encoding one logical qubit into multiple physical qubits:

- **3-qubit code**: Can correct 1 bit-flip error
- **5-qubit code**: Can correct 2 bit-flip errors  
- **7-qubit code**: Can correct 3 bit-flip errors

#### How It Works

1. **Encoding**: A logical qubit state |ψ⟩ = α|0⟩ + β|1⟩ is encoded into n physical qubits:
   - |0⟩ → |000...0⟩
   - |1⟩ → |111...1⟩

2. **Error Detection**: Syndrome measurements detect errors without collapsing the quantum state. We measure the parity between adjacent qubits.

3. **Error Correction**: Using majority voting, we decode the logical qubit value from the physical qubits.

### Bit-Flip Errors

A bit-flip error is represented by the Pauli X operator:
- X|0⟩ = |1⟩
- X|1⟩ = |0⟩

### Phase-Flip Errors

A phase-flip error is represented by the Pauli Z operator:
- Z|0⟩ = |0⟩
- Z|1⟩ = -|1⟩

In the Hadamard basis (|+⟩, |-⟩), a phase-flip acts like a bit-flip:
- Z|+⟩ = |-⟩
- Z|-⟩ = |+⟩

Our Phase-Flip Repetition Code protects against these Z errors by encoding logical qubits in the X-basis (|+⟩, |-⟩).

In our simulations, each physical qubit has a probability `p` of experiencing an error (X or Z depending on the code).

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone or download this repository**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   This will install:
   - `stim` - High-performance quantum circuit simulator
   - `numpy` - Numerical computing
   - `matplotlib` - Visualization

## 📁 Project Structure

```
Project1/
├── src/
│   ├── __init__.py              # Package initialization
│   ├── repetition_code.py       # Repetition code implementation
│   ├── error_simulation.py      # Error injection and simulation
│   ├── decoder.py               # Majority voting decoder
│   └── analysis.py              # Performance analysis and visualization
├── examples/
│   ├── basic_demo.py            # Simple demonstration
│   └── comprehensive_analysis.py # Full analysis with plots
├── results/                     # Generated plots (created automatically)
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 💻 Usage

### Basic Demo

Run a simple demonstration showing error correction in action:

```bash
cd examples
python basic_demo.py
```

**Output:**
- Comparison of protected vs unprotected error rates
- Circuit structure visualization
- Success/failure indication

### Comprehensive Analysis

Run a full analysis comparing different code sizes and generating plots:

```bash
cd examples
python comprehensive_analysis.py
```

**This will:**
1. Test 3-qubit, 5-qubit, and 7-qubit repetition codes
2. Sweep over noise probabilities from 0.1% to 20%
3. Compare protected vs unprotected qubits
4. Analyze measurement error impact
5. Generate visualization plots in `results/` directory

**Generated Plots:**
- `protected_vs_unprotected_d3.png` - 3-qubit code performance
- `protected_vs_unprotected_d5.png` - 5-qubit code performance
- `protected_vs_unprotected_d7.png` - 7-qubit code performance
- `code_size_comparison.png` - All code sizes compared
- `measurement_error_impact_d5.png` - Measurement noise analysis

## 📊 Example Results

### Protected vs Unprotected

At moderate noise levels (e.g., 5% bit-flip probability):
- **Unprotected qubit**: ~5% error rate
- **5-qubit repetition code**: ~0.5% error rate
- **Improvement**: ~90% reduction in errors!

### Code Size Impact

Larger codes provide better protection:
- **3-qubit code**: Effective up to ~10% physical error rate
- **5-qubit code**: Effective up to ~15% physical error rate
- **7-qubit code**: Effective up to ~18% physical error rate

### Measurement Errors

Measurement errors degrade performance:
- At 0% measurement error: Best performance
- At 5% measurement error: Significant degradation
- Trade-off between code size and measurement accuracy

### Phase-Flip Protection

The project now supports protection against Phase-Flip (Z) errors using X-basis encoding regarding.

![Phase Flip Results](results/phase_flip_comparison.png)

*Comparison of Phase-Flip Code (d=5) vs Unprotected Qubit under Z-noise.*

## 🔬 Key Concepts Demonstrated

### 1. Error Threshold

Below a certain physical error rate (the **threshold**), error correction reduces logical error rates. Above this threshold, adding more qubits actually increases errors due to the overhead.

### 2. Code Distance

The **code distance** `d` determines how many errors can be corrected:
- Can correct up to `(d-1)/2` errors
- Larger distance = better protection but more overhead

### 3. Syndrome Measurement

**Syndrome measurements** detect errors without measuring the data qubits directly, preserving the quantum state.

### 4. Majority Voting

The **decoder** uses majority voting to determine the logical qubit value from the physical qubits.

## 🛠️ Customization

### Modify Parameters

Edit the scripts to test different configurations:

```python
# In basic_demo.py or comprehensive_analysis.py
code_distance = 7          # Change code size
noise_prob = 0.05          # Change error probability
num_shots = 20000          # More shots = better statistics
```

### Add New Code Types

Extend `repetition_code.py` to implement other codes:
- Phase-flip codes
- Shor's 9-qubit code
- Surface codes (advanced)

## 📖 References

### Papers & Books
- Nielsen & Chuang, "Quantum Computation and Quantum Information"
- Preskill, "Quantum Computing in the NISQ era and beyond"

### Stim Documentation
- [Stim GitHub](https://github.com/quantumlib/Stim)
- [Stim Documentation](https://github.com/quantumlib/Stim/blob/main/doc/getting_started.md)

### Quantum Error Correction
- [Introduction to QEC](https://en.wikipedia.org/wiki/Quantum_error_correction)
- [Repetition Codes](https://en.wikipedia.org/wiki/Quantum_error_correction#Repetition_code)

## 🎓 Learning Outcomes

By completing this project, you will:
- ✅ Understand basic quantum error correction principles
- ✅ Gain hands-on experience with quantum circuit simulation
- ✅ Learn how to model and analyze quantum noise
- ✅ Develop skills in quantum algorithm evaluation
- ✅ Practice scientific computing with Python

## 🤝 Contributing

This is a beginner educational project. Feel free to:
- Add more error models (phase-flip, depolarizing)
- Implement different decoders
- Add more visualization options
- Improve documentation

## 📝 License

This project is open source and available for educational purposes.

## 👤 Author

**Param Parekh**

Stony Brook University - Quantum Computing Research

---

**Happy Quantum Computing! 🚀**
