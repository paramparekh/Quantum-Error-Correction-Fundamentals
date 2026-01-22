"""
Basic Quantum Error Correction Demo

This script demonstrates basic quantum error correction using a repetition code.
It shows how error correction can protect against bit-flip noise.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.repetition_code import RepetitionCode, UnprotectedQubit
from src.error_simulation import run_error_correction_simulation, run_unprotected_simulation
from src.decoder import calculate_logical_error_rate
import numpy as np


def main():
    """Run a basic demonstration of quantum error correction."""
    
    print("=" * 70)
    print("QUANTUM ERROR CORRECTION DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Parameters
    code_distance = 5
    noise_prob = 0.1  # 10% bit-flip error probability
    num_shots = 10000
    
    print(f"Configuration:")
    print(f"  Code distance: {code_distance} qubits")
    print(f"  Bit-flip error probability: {noise_prob * 100}%")
    print(f"  Number of shots: {num_shots}")
    print()
    
    # Create repetition code
    print(f"Creating {code_distance}-qubit repetition code...")
    code = RepetitionCode(code_distance)
    print(f"  Number of data qubits: {code.num_qubits}")
    print(f"  Number of syndrome measurements: {code.num_ancillas}")
    print()
    
    # Run protected simulation
    print("Running error correction simulation...")
    protected_samples, circuit = run_error_correction_simulation(
        code, noise_prob, num_shots=num_shots
    )
    
    # Calculate logical error rate
    logical_error_rate = calculate_logical_error_rate(protected_samples, code_distance)
    print(f"  Logical error rate (protected): {logical_error_rate:.4f} ({logical_error_rate * 100:.2f}%)")
    print()
    
    # Run unprotected simulation for comparison
    print("Running unprotected qubit simulation...")
    unprotected_samples, _ = run_unprotected_simulation(noise_prob, num_shots=num_shots)
    physical_error_rate = np.mean(unprotected_samples)
    print(f"  Physical error rate (unprotected): {physical_error_rate:.4f} ({physical_error_rate * 100:.2f}%)")
    print()
    
    # Compare results
    print("=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)
    print()
    print(f"Physical error probability: {noise_prob * 100}%")
    print(f"Unprotected error rate: {physical_error_rate * 100:.2f}%")
    print(f"Protected error rate: {logical_error_rate * 100:.2f}%")
    
    if logical_error_rate < physical_error_rate:
        improvement = (physical_error_rate - logical_error_rate) / physical_error_rate * 100
        print(f"\n✓ Error correction SUCCESSFUL!")
        print(f"  Error rate reduced by {improvement:.1f}%")
    else:
        print(f"\n✗ Error correction did not improve performance at this noise level.")
        print(f"  (Noise is too high for this code distance)")
    
    print()
    print("=" * 70)
    
    # Show circuit structure
    print("\nCircuit Structure:")
    print("-" * 70)
    print(circuit)
    print("-" * 70)


if __name__ == "__main__":
    main()
