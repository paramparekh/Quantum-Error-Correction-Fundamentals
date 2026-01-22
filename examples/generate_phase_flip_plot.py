"""
Generate Phase-Flip Comparison Plot

This script runs simulations for phase-flip errors and generates a comparison plot
between protected (Phase-Flip Code) and unprotected qubits.
"""

import sys
import os
import matplotlib.pyplot as plt
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.repetition_code import RepetitionCode
from src.error_simulation import run_error_correction_simulation, run_unprotected_simulation
from src.decoder import calculate_logical_error_rate
from src.analysis import PerformanceAnalyzer

def main():
    print("Generating Phase-Flip comparison plot...")
    
    # Parameters
    code_distance = 5
    noise_probs = [0.001, 0.005, 0.01, 0.02, 0.05, 0.1, 0.15, 0.2]
    num_shots = 10000
    basis = 'x'  # Phase-Flip
    
    protected_rates = []
    unprotected_rates = []
    
    code = RepetitionCode(code_distance, basis=basis)
    
    for p in noise_probs:
        print(f"  Simulating p={p}...")
        
        # Protected
        samples, _ = run_error_correction_simulation(code, p, num_shots=num_shots)
        p_rate = calculate_logical_error_rate(samples, code_distance)
        protected_rates.append(p_rate)
        
        # Unprotected
        u_samples, _ = run_unprotected_simulation(p, num_shots=num_shots, basis=basis)
        u_rate = np.mean(u_samples)
        unprotected_rates.append(u_rate)
        
    # Plotting
    output_dir = 'results'
    os.makedirs(output_dir, exist_ok=True)
    
    plt.figure(figsize=(10, 6))
    
    plt.plot(noise_probs, unprotected_rates, 'o-', label='Unprotected Qubit (Z-noise)', 
            linewidth=2, markersize=8, color='red')
    plt.plot(noise_probs, protected_rates, 's-', 
            label=f'Protected ({code_distance}-qubit Phase-Flip Code)', 
            linewidth=2, markersize=8, color='blue')
    
    plt.xlabel('Phase-Flip Error Probability', fontsize=12)
    plt.ylabel('Logical Error Rate', fontsize=12)
    plt.title(f'Phase-Flip Error Correction Performance (d={code_distance})', 
             fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.yscale('log')
    plt.xscale('log')
    
    # Add threshold line
    plt.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5, label='Random guess')
    
    filename = os.path.join(output_dir, 'phase_flip_comparison.png')
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Plot saved to {filename}")

if __name__ == "__main__":
    main()
