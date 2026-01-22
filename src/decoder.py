"""
Decoder Module

This module implements error correction decoders for repetition codes.
The decoder interprets syndrome measurements and corrects errors.
"""

import numpy as np
from typing import List


class MajorityVoteDecoder:
    """
    Implements majority voting decoder for repetition codes.
    
    The decoder looks at all physical qubit measurements and returns
    the majority value as the logical qubit value.
    """
    
    def __init__(self, code_distance):
        """
        Initialize the decoder.
        
        Args:
            code_distance (int): Number of physical qubits in the code
        """
        self.code_distance = code_distance
        self.num_syndrome_measurements = code_distance - 1
    
    def decode(self, syndrome, data_measurements):
        """
        Decode the logical qubit value using majority voting.
        
        Args:
            syndrome (numpy.ndarray): Syndrome measurement results
            data_measurements (numpy.ndarray): Final data qubit measurements
            
        Returns:
            int: Decoded logical value (0 or 1)
        """
        # Simple majority vote on data measurements
        ones_count = np.sum(data_measurements)
        zeros_count = len(data_measurements) - ones_count
        
        # Return the majority value
        return 1 if ones_count > zeros_count else 0
    
    def decode_with_syndrome(self, syndrome, data_measurements):
        """
        Decode using both syndrome and data measurements.
        
        This is a more sophisticated approach that uses syndrome information
        to identify likely error locations.
        
        Args:
            syndrome (numpy.ndarray): Syndrome measurement results
            data_measurements (numpy.ndarray): Final data qubit measurements
            
        Returns:
            int: Decoded logical value (0 or 1)
        """
        # For repetition codes, syndrome tells us where bit flips occurred
        # syndrome[i] = 1 means qubits i and i+1 differ
        
        # Start with the data measurements
        corrected_data = data_measurements.copy()
        
        # Use syndrome to identify error patterns
        # For simplicity, we'll use majority voting
        # More sophisticated decoders could use the syndrome more effectively
        
        return self.decode(syndrome, data_measurements)


def create_decoder(code_distance):
    """
    Factory function to create a decoder for a given code distance.
    
    Args:
        code_distance (int): Number of physical qubits
        
    Returns:
        MajorityVoteDecoder: Initialized decoder
    """
    return MajorityVoteDecoder(code_distance)


def decode_samples(samples, code_distance):
    """
    Decode multiple samples using majority voting.
    
    Args:
        samples (numpy.ndarray): Array of measurement samples
        code_distance (int): Number of physical qubits
        
    Returns:
        numpy.ndarray: Array of decoded logical values
    """
    decoder = create_decoder(code_distance)
    num_syndrome = code_distance - 1
    
    decoded_values = []
    
    for sample in samples:
        syndrome = sample[:num_syndrome]
        data = sample[num_syndrome:]
        decoded_value = decoder.decode(syndrome, data)
        decoded_values.append(decoded_value)
    
    return np.array(decoded_values)


def calculate_logical_error_rate(samples, code_distance, expected_value=0):
    """
    Calculate the logical error rate after decoding.
    
    Args:
        samples (numpy.ndarray): Measurement samples
        code_distance (int): Number of physical qubits
        expected_value (int): Expected logical value (0 or 1)
        
    Returns:
        float: Logical error rate
    """
    decoded_values = decode_samples(samples, code_distance)
    errors = np.sum(decoded_values != expected_value)
    return errors / len(decoded_values)


def analyze_syndrome_patterns(samples, code_distance):
    """
    Analyze syndrome patterns to understand error distributions.
    
    Args:
        samples (numpy.ndarray): Measurement samples
        code_distance (int): Number of physical qubits
        
    Returns:
        dict: Statistics about syndrome patterns
    """
    num_syndrome = code_distance - 1
    syndrome_counts = {}
    
    for sample in samples:
        syndrome = tuple(sample[:num_syndrome])
        syndrome_counts[syndrome] = syndrome_counts.get(syndrome, 0) + 1
    
    # Calculate statistics
    total_samples = len(samples)
    syndrome_stats = {
        'patterns': syndrome_counts,
        'num_unique_patterns': len(syndrome_counts),
        'most_common': max(syndrome_counts.items(), key=lambda x: x[1]),
        'total_samples': total_samples
    }
    
    return syndrome_stats
