"""
Comprehensive Quantum Error Correction Analysis

This script runs a complete analysis of quantum error correction performance,
comparing different code sizes and noise levels, and generates visualization plots.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.analysis import run_comprehensive_analysis
from src.repetition_code import RepetitionCode
from src.error_simulation import run_error_correction_simulation
from src.decoder import calculate_logical_error_rate
from src.analysis import PerformanceAnalyzer
import numpy as np


def analyze_measurement_error_impact():
    """Analyze how measurement errors affect performance."""
    
    print("\n" + "=" * 70)
    print("MEASUREMENT ERROR IMPACT ANALYSIS")
    print("=" * 70)
    print()
    
    code_distance = 5
    noise_prob = 0.05  # Fixed physical error rate
    measurement_errors = [0.0, 0.001, 0.005, 0.01, 0.02, 0.05]
    num_shots = 10000
    
    print(f"Configuration:")
    print(f"  Code distance: {code_distance}")
    print(f"  Physical error rate: {noise_prob * 100}%")
    print(f"  Measurement error rates: {[m * 100 for m in measurement_errors]}%")
    print()
    
    code = RepetitionCode(code_distance)
    logical_error_rates = []
    
    for meas_error in measurement_errors:
        print(f"Testing measurement error = {meas_error * 100}%...")
        samples, _ = run_error_correction_simulation(
            code, noise_prob, measurement_noise=meas_error, num_shots=num_shots
        )
        logical_error_rate = calculate_logical_error_rate(samples, code_distance)
        logical_error_rates.append(logical_error_rate)
        print(f"  Logical error rate: {logical_error_rate:.4f}")
    
    # Generate plot
    analyzer = PerformanceAnalyzer('results')
    analyzer.plot_measurement_error_impact(
        noise_prob, measurement_errors, logical_error_rates, code_distance
    )
    
    print("\nMeasurement error analysis complete!")


def main():
    """Run comprehensive quantum error correction analysis."""
    
    print("=" * 70)
    print("COMPREHENSIVE QUANTUM ERROR CORRECTION ANALYSIS")
    print("=" * 70)
    print()
    print("This script will:")
    print("  1. Compare different repetition code sizes (3, 5, 7 qubits)")
    print("  2. Sweep over various noise probabilities")
    print("  3. Compare protected vs unprotected qubits")
    print("  4. Analyze measurement error impact")
    print("  5. Generate visualization plots")
    print()
    # input("Press Enter to continue...")
    print()
    
    # Main analysis: compare code sizes
    code_distances = [3, 5, 7]
    noise_probs = [0.001, 0.005, 0.01, 0.02, 0.05, 0.1, 0.15, 0.2]
    num_shots = 10000
    
    results = run_comprehensive_analysis(
        code_distances=code_distances,
        noise_probs=noise_probs,
        num_shots=num_shots,
        output_dir='results'
    )
    
    # Additional analysis: measurement errors
    analyze_measurement_error_impact()
    
    # Print summary
    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)
    print()
    print("Generated plots:")
    print("  - protected_vs_unprotected_d3.png")
    print("  - protected_vs_unprotected_d5.png")
    print("  - protected_vs_unprotected_d7.png")
    print("  - code_size_comparison.png")
    print("  - measurement_error_impact_d5.png")
    print()
    print("All plots saved to 'results/' directory.")
    print()
    
    # Print key findings
    print("KEY FINDINGS:")
    print("-" * 70)
    
    for distance in code_distances:
        protected = results[f'd{distance}_protected']
        unprotected = results[f'd{distance}_unprotected']
        
        # Find the noise level where protection is most effective
        improvements = [(u - p) / u * 100 for u, p in zip(unprotected, protected)]
        best_idx = np.argmax(improvements)
        best_noise = noise_probs[best_idx]
        best_improvement = improvements[best_idx]
        
        print(f"\n{distance}-qubit code:")
        print(f"  Best performance at p = {best_noise:.3f}")
        print(f"  Error rate reduction: {best_improvement:.1f}%")
        print(f"  Logical error rate: {protected[best_idx]:.4f}")
        print(f"  Physical error rate: {unprotected[best_idx]:.4f}")
    
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
