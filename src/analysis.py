"""
Analysis Module

This module provides tools for analyzing quantum error correction performance
and generating visualizations.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple
import os


class PerformanceAnalyzer:
    """
    Analyzes quantum error correction performance and generates reports.
    """
    
    def __init__(self, output_dir='results'):
        """
        Initialize the analyzer.
        
        Args:
            output_dir (str): Directory to save plots and results
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def compare_protected_vs_unprotected(self, noise_probs, protected_rates, 
                                        unprotected_rates, code_distance):
        """
        Create a comparison plot of protected vs unprotected error rates.
        
        Args:
            noise_probs (list): List of noise probabilities
            protected_rates (list): Logical error rates for protected qubits
            unprotected_rates (list): Error rates for unprotected qubits
            code_distance (int): Code distance used
        """
        plt.figure(figsize=(10, 6))
        
        plt.plot(noise_probs, unprotected_rates, 'o-', label='Unprotected Qubit', 
                linewidth=2, markersize=8, color='red')
        plt.plot(noise_probs, protected_rates, 's-', 
                label=f'Protected ({code_distance}-qubit code)', 
                linewidth=2, markersize=8, color='blue')
        
        plt.xlabel('Physical Error Rate (Bit-Flip Probability)', fontsize=12)
        plt.ylabel('Logical Error Rate', fontsize=12)
        plt.title(f'Error Correction Performance: {code_distance}-Qubit Repetition Code', 
                 fontsize=14, fontweight='bold')
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3)
        plt.yscale('log')
        plt.xscale('log')
        
        # Add threshold line
        plt.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5, 
                   label='Random guess (50%)')
        
        filename = os.path.join(self.output_dir, 
                               f'protected_vs_unprotected_d{code_distance}.png')
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Saved comparison plot: {filename}")
    
    def compare_code_sizes(self, noise_probs, error_rates_by_distance, 
                          unprotected_rates=None):
        """
        Compare different code sizes on the same plot.
        
        Args:
            noise_probs (list): List of noise probabilities
            error_rates_by_distance (dict): Dict mapping code_distance to error rates
            unprotected_rates (list, optional): Unprotected error rates for reference
        """
        plt.figure(figsize=(12, 7))
        
        colors = ['blue', 'green', 'purple', 'orange']
        markers = ['s', 'o', '^', 'd']
        
        # Plot protected codes
        for idx, (distance, rates) in enumerate(sorted(error_rates_by_distance.items())):
            plt.plot(noise_probs, rates, 
                    marker=markers[idx % len(markers)],
                    label=f'{distance}-qubit code',
                    linewidth=2, markersize=8,
                    color=colors[idx % len(colors)])
        
        # Plot unprotected if provided
        if unprotected_rates is not None:
            plt.plot(noise_probs, unprotected_rates, 'o-', 
                    label='Unprotected', linewidth=2, markersize=8, 
                    color='red', alpha=0.7)
        
        plt.xlabel('Physical Error Rate (Bit-Flip Probability)', fontsize=12)
        plt.ylabel('Logical Error Rate', fontsize=12)
        plt.title('Code Size Comparison: Repetition Codes', 
                 fontsize=14, fontweight='bold')
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3)
        plt.yscale('log')
        plt.xscale('log')
        
        filename = os.path.join(self.output_dir, 'code_size_comparison.png')
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Saved code size comparison: {filename}")
    
    def plot_measurement_error_impact(self, noise_prob, measurement_errors, 
                                     logical_error_rates, code_distance):
        """
        Plot the impact of measurement errors on performance.
        
        Args:
            noise_prob (float): Fixed physical error rate
            measurement_errors (list): List of measurement error probabilities
            logical_error_rates (list): Corresponding logical error rates
            code_distance (int): Code distance used
        """
        plt.figure(figsize=(10, 6))
        
        plt.plot(measurement_errors, logical_error_rates, 'o-', 
                linewidth=2, markersize=8, color='purple')
        
        plt.xlabel('Measurement Error Probability', fontsize=12)
        plt.ylabel('Logical Error Rate', fontsize=12)
        plt.title(f'Impact of Measurement Errors ({code_distance}-qubit code, ' + 
                 f'p_phys = {noise_prob})', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        
        filename = os.path.join(self.output_dir, 
                               f'measurement_error_impact_d{code_distance}.png')
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Saved measurement error impact plot: {filename}")
    
    def generate_summary_report(self, results_dict, filename='summary_report.txt'):
        """
        Generate a text summary of results.
        
        Args:
            results_dict (dict): Dictionary containing analysis results
            filename (str): Output filename
        """
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write("=" * 70 + "\n")
            f.write("QUANTUM ERROR CORRECTION SIMULATION RESULTS\n")
            f.write("=" * 70 + "\n\n")
            
            for key, value in results_dict.items():
                f.write(f"{key}:\n")
                if isinstance(value, dict):
                    for k, v in value.items():
                        f.write(f"  {k}: {v}\n")
                else:
                    f.write(f"  {value}\n")
                f.write("\n")
        
        print(f"Saved summary report: {filepath}")


def calculate_error_rates_from_samples(samples_list, code_distances, expected_value=0):
    """
    Calculate error rates from multiple sample sets.
    
    Args:
        samples_list (list): List of sample arrays
        code_distances (list): Corresponding code distances
        expected_value (int): Expected logical value
        
    Returns:
        list: Error rates for each sample set
    """
    from .decoder import calculate_logical_error_rate
    
    error_rates = []
    
    for samples, distance in zip(samples_list, code_distances):
        rate = calculate_logical_error_rate(samples, distance, expected_value)
        error_rates.append(rate)
    
    return error_rates


def run_comprehensive_analysis(code_distances=[3, 5, 7], 
                               noise_probs=None,
                               num_shots=10000,
                               output_dir='results'):
    """
    Run a comprehensive analysis of quantum error correction performance.
    
    Args:
        code_distances (list): List of code distances to test
        noise_probs (list): List of noise probabilities to sweep
        num_shots (int): Number of shots per simulation
        output_dir (str): Directory for output files
        
    Returns:
        dict: Complete analysis results
    """
    from .repetition_code import RepetitionCode
    from .error_simulation import (run_error_correction_simulation, 
                                   run_unprotected_simulation)
    from .decoder import calculate_logical_error_rate
    
    if noise_probs is None:
        noise_probs = [0.001, 0.005, 0.01, 0.02, 0.05, 0.1, 0.15, 0.2]
    
    analyzer = PerformanceAnalyzer(output_dir)
    results = {}
    
    print("Running comprehensive quantum error correction analysis...")
    print(f"Code distances: {code_distances}")
    print(f"Noise probabilities: {noise_probs}")
    print(f"Shots per simulation: {num_shots}\n")
    
    # Compare each code size against unprotected
    for distance in code_distances:
        print(f"\nAnalyzing {distance}-qubit repetition code...")
        code = RepetitionCode(distance)
        
        protected_rates = []
        unprotected_rates = []
        
        for noise_prob in noise_probs:
            # Protected qubit
            samples, _ = run_error_correction_simulation(code, noise_prob, 
                                                         num_shots=num_shots)
            logical_error_rate = calculate_logical_error_rate(samples, distance)
            protected_rates.append(logical_error_rate)
            
            # Unprotected qubit
            unprotected_samples, _ = run_unprotected_simulation(noise_prob, 
                                                                num_shots=num_shots)
            physical_error_rate = np.mean(unprotected_samples)
            unprotected_rates.append(physical_error_rate)
            
            print(f"  p={noise_prob:.3f}: Protected={logical_error_rate:.4f}, " + 
                  f"Unprotected={physical_error_rate:.4f}")
        
        # Save individual comparison
        analyzer.compare_protected_vs_unprotected(noise_probs, protected_rates,
                                                  unprotected_rates, distance)
        
        results[f'd{distance}_protected'] = protected_rates
        results[f'd{distance}_unprotected'] = unprotected_rates
    
    # Compare all code sizes
    print("\nGenerating code size comparison...")
    error_rates_by_distance = {
        distance: results[f'd{distance}_protected'] 
        for distance in code_distances
    }
    analyzer.compare_code_sizes(noise_probs, error_rates_by_distance, 
                               results[f'd{code_distances[0]}_unprotected'])
    
    # Store metadata
    results['metadata'] = {
        'code_distances': code_distances,
        'noise_probs': noise_probs,
        'num_shots': num_shots
    }
    
    print(f"\nAnalysis complete! Results saved to '{output_dir}/' directory.")
    
    return results
