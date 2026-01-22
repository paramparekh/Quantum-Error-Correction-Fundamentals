"""
Error Simulation Module

This module handles error injection and simulation for quantum circuits.
It provides tools to simulate bit-flip errors and measurement errors.
"""

import stim
import numpy as np
from typing import Tuple, List


class ErrorSimulator:
    """
    Simulates quantum errors and runs circuit simulations.
    """
    
    def __init__(self, num_shots=10000):
        """
        Initialize the error simulator.
        
        Args:
            num_shots (int): Number of simulation runs for statistical analysis
        """
        self.num_shots = num_shots
    
    def simulate_circuit(self, circuit):
        """
        Simulate a quantum circuit and collect measurement results.
        
        Args:
            circuit (stim.Circuit): The circuit to simulate
            
        Returns:
            numpy.ndarray: Measurement results (num_shots x num_measurements)
        """
        sampler = circuit.compile_sampler()
        samples = sampler.sample(shots=self.num_shots)
        return samples
    
    def calculate_logical_error_rate(self, samples, num_syndrome_measurements, decoder_func):
        """
        Calculate the logical error rate after error correction.
        
        Args:
            samples (numpy.ndarray): Measurement samples
            num_syndrome_measurements (int): Number of syndrome measurements
            decoder_func (callable): Function to decode syndrome and data measurements
            
        Returns:
            float: Logical error rate (fraction of errors after correction)
        """
        num_errors = 0
        
        for sample in samples:
            # Split syndrome and data measurements
            syndrome = sample[:num_syndrome_measurements]
            data = sample[num_syndrome_measurements:]
            
            # Decode to get the corrected logical value
            corrected_value = decoder_func(syndrome, data)
            
            # Expected logical value is 0 (we initialized to |0⟩)
            if corrected_value != 0:
                num_errors += 1
        
        return num_errors / len(samples)
    
    def calculate_physical_error_rate(self, samples):
        """
        Calculate the physical error rate (for unprotected qubits).
        
        Args:
            samples (numpy.ndarray): Measurement samples (single qubit)
            
        Returns:
            float: Physical error rate
        """
        # Count how many times we measured 1 (error occurred)
        num_errors = np.sum(samples)
        return num_errors / len(samples)


def run_error_correction_simulation(code, noise_prob, measurement_noise=0.0, num_shots=10000):
    """
    Run a complete error correction simulation.
    
    Args:
        code: RepetitionCode instance
        noise_prob (float): Bit-flip error probability
        measurement_noise (float): Measurement error probability
        num_shots (int): Number of simulation runs
        
    Returns:
        Tuple[numpy.ndarray, stim.Circuit]: Samples and circuit used
    """
    circuit = code.create_full_circuit(noise_prob, measurement_noise)
    simulator = ErrorSimulator(num_shots)
    samples = simulator.simulate_circuit(circuit)
    
    return samples, circuit


def run_unprotected_simulation(noise_prob, num_shots=10000, basis='z'):
    """
    Run simulation for an unprotected qubit.
    
    Args:
        noise_prob (float): Error probability
        num_shots (int): Number of simulation runs
        basis (str): 'z' or 'x'
        
    Returns:
        Tuple[numpy.ndarray, stim.Circuit]: Samples and circuit used
    """
    from .repetition_code import UnprotectedQubit
    
    unprotected = UnprotectedQubit(basis=basis)
    circuit = unprotected.create_circuit(noise_prob)
    simulator = ErrorSimulator(num_shots)
    samples = simulator.simulate_circuit(circuit)
    
    return samples, circuit


def sweep_noise_probabilities(code, noise_probs, measurement_noise=0.0, num_shots=10000):
    """
    Sweep over different noise probabilities and collect error rates.
    
    Args:
        code: RepetitionCode instance
        noise_probs (list): List of noise probabilities to test
        measurement_noise (float): Measurement error probability
        num_shots (int): Number of shots per simulation
        
    Returns:
        List[Tuple[float, numpy.ndarray]]: List of (noise_prob, samples) pairs
    """
    results = []
    
    for noise_prob in noise_probs:
        samples, _ = run_error_correction_simulation(
            code, noise_prob, measurement_noise, num_shots
        )
        results.append((noise_prob, samples))
    
    return results


def compare_code_sizes(code_distances, noise_prob, measurement_noise=0.0, num_shots=10000):
    """
    Compare different repetition code sizes at a fixed noise level.
    
    Args:
        code_distances (list): List of code distances to compare
        noise_prob (float): Bit-flip error probability
        measurement_noise (float): Measurement error probability
        num_shots (int): Number of shots per simulation
        
    Returns:
        dict: Dictionary mapping code_distance to samples
    """
    from .repetition_code import RepetitionCode
    
    results = {}
    
    for distance in code_distances:
        code = RepetitionCode(distance)
        samples, _ = run_error_correction_simulation(
            code, noise_prob, measurement_noise, num_shots
        )
        results[distance] = samples
    
    return results
