"""
Phase-Flip Error Correction Demo

This script demonstrates quantum error correction protecting against phase-flip (Z) errors.
It uses the Phase-Flip Repetition Code, which operates in the X-basis.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.repetition_code import RepetitionCode
from src.error_simulation import run_error_correction_simulation, run_unprotected_simulation
from src.decoder import calculate_logical_error_rate
import numpy as np


def main():
    """Run a demonstration of Phase-Flip error correction."""
    
    print("=" * 70)
    print("PHASE-FLIP ERROR CORRECTION DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Parameters
    code_distance = 5
    noise_prob = 0.1  # 10% phase-flip (Z) error probability
    num_shots = 10000
    basis = 'x'       # 'x' basis for Phase-Flip code
    
    print(f"Configuration:")
    print(f"  Code Type: Phase-Flip Repetition Code (X-basis)")
    print(f"  Code distance: {code_distance} qubits")
    print(f"  Phase-flip (Z) error probability: {noise_prob * 100}%")
    print(f"  Number of shots: {num_shots}")
    print()
    
    # Create repetition code
    print(f"Creating {code_distance}-qubit phase-flip repetition code...")
    code = RepetitionCode(code_distance, basis=basis)
    print(f"  Number of physical qubits: {code.num_qubits}")
    print()
    
    # Run protected simulation
    print("Running phase-flip error correction simulation...")
    protected_samples, circuit = run_error_correction_simulation(
        code, noise_prob, num_shots=num_shots
    )
    
    # Calculate logical error rate
    # Note: Majority vote works the same way because we map |+> to 0 and |-> to 1
    logical_error_rate = calculate_logical_error_rate(protected_samples, code_distance)
    print(f"  Logical error rate (protected): {logical_error_rate:.4f} ({logical_error_rate * 100:.2f}%)")
    print()
    
    # Run unprotected simulation for comparison
    print("Running unprotected qubit simulation (under Z-noise)...")
    unprotected_samples, _ = run_unprotected_simulation(noise_prob, num_shots=num_shots, basis=basis)
    physical_error_rate = np.mean(unprotected_samples)
    print(f"  Physical error rate (unprotected): {physical_error_rate:.4f} ({physical_error_rate * 100:.2f}%)")
    print()
    
    # Compare results
    print("=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)
    print()
    print(f"Phase-Flip error probability: {noise_prob * 100}%")
    print(f"Unprotected error rate: {physical_error_rate * 100:.2f}%")
    print(f"Protected error rate: {logical_error_rate * 100:.2f}%")
    
    if logical_error_rate < physical_error_rate:
        improvement = (physical_error_rate - logical_error_rate) / physical_error_rate * 100
        print(f"\n✓ Phase-Flip Error Correction SUCCESSFUL!")
        print(f"  Error rate reduced by {improvement:.1f}%")
    else:
        print(f"\n✗ Error correction did not improve performance.")
    
    print()
    print("=" * 70)
    
    # Show circuit structure (optional, truncated)
    # print("\nCircuit Structure (Truncated):")
    # print(circuit)


if __name__ == "__main__":
    main()
