"""
Repetition Code Implementation

This module implements quantum repetition codes for error correction.
Repetition codes encode a logical qubit into multiple physical qubits
to protect against bit-flip errors.
"""

import stim
import numpy as np


class RepetitionCode:
    """
    Implements a quantum repetition code for bit-flip error correction.
    
    The repetition code encodes one logical qubit into n physical qubits,
    where n is odd (typically 3, 5, or 7). It can correct up to (n-1)/2
    bit-flip errors.
    """
    
    def __init__(self, code_distance, basis='z'):
        """
        Initialize a repetition code.
        
        Args:
            code_distance (int): Number of physical qubits (must be odd, >= 3)
            basis (str): 'z' for bit-flip code (protects against X errors),
                         'x' for phase-flip code (protects against Z errors).
        """
        if code_distance < 3 or code_distance % 2 == 0:
            raise ValueError("Code distance must be odd and >= 3")
        if basis not in ['z', 'x']:
            raise ValueError("Basis must be 'z' or 'x'")
        
        self.code_distance = code_distance
        self.num_qubits = code_distance
        self.num_ancillas = code_distance - 1  # For syndrome measurement
        self.basis = basis
    
    def create_encoding_circuit(self, initial_state='0'):
        """
        Create a circuit that encodes a logical qubit into the repetition code.
        
        Args:
            initial_state (str): Initial logical state ('0' or '1')
            
        Returns:
            stim.Circuit: The encoding circuit
        """
        circuit = stim.Circuit()
        
        # Initialize the first qubit to the desired state
        if initial_state == '1':
            circuit.append("X", [0])
        
        # Encode by applying CNOT gates to spread the state
        for i in range(1, self.num_qubits):
            circuit.append("CNOT", [0, i])
            
        # If using Phase-Flip code (X basis), apply H to all qubits
        # This transforms the logical |0> (|00...0>) into |+>_L (|++...+>)
        if self.basis == 'x':
            for i in range(self.num_qubits):
                circuit.append("H", [i])
        
        return circuit
    
    def create_syndrome_measurement_circuit(self, noise_prob=0.0, measurement_noise=0.0):
        """
        Create a circuit for syndrome measurement.
        
        Args:
            noise_prob (float): Probability of error (X for basis='z', Z for basis='x')
            measurement_noise (float): Probability of measurement error
            
        Returns:
            stim.Circuit: Complete circuit with encoding, noise, and syndrome measurement
        """
        circuit = stim.Circuit()
        
        # 1. Encoding
        # Standard |0> encoding
        for i in range(1, self.num_qubits):
            circuit.append("CNOT", [0, i])
            
        # If X-basis code, rotate to X-basis
        if self.basis == 'x':
            for i in range(self.num_qubits):
                circuit.append("H", [i])
        
        # 2. Noise
        # Add noise relevant to the code
        noise_op = "X_ERROR" if self.basis == 'z' else "Z_ERROR"
        if noise_prob > 0:
            for i in range(self.num_qubits):
                circuit.append(noise_op, [i], noise_prob)
        
        # 3. Syndrome Measurement
        # We assume ancillas are 0.
        ancilla_offset = self.num_qubits
        
        # If X-basis code, we need to measure X-parity (ZZ..Z in X-basis is XX..X in Z-basis)
        # To measure X-parity using CNOTs (which measure Z-parity), we need to rotate data to Z-basis temporarily
        if self.basis == 'x':
             for i in range(self.num_qubits):
                circuit.append("H", [i])
        
        for i in range(self.num_ancillas):
            # Reset ancilla
            circuit.append("R", [ancilla_offset + i])
            
            # Measure parity between qubits i and i+1
            # For Z-basis code: Checks Z_i Z_{i+1} parity
            # For X-basis code (after H): Checks X_i X_{i+1} parity
            circuit.append("CNOT", [i, ancilla_offset + i])
            circuit.append("CNOT", [i + 1, ancilla_offset + i])
            
            # Measure ancilla
            if measurement_noise > 0:
                circuit.append("X_ERROR", [ancilla_offset + i], measurement_noise)
            circuit.append("M", [ancilla_offset + i])
            
        # If X-basis code, rotate back to X-basis if we were continuing
        # But since we are just measuring immediately after, we can choose to measure in X basis
        # However, for consistency with 'decoding', let's stick to the convention:
        # Measure data qubits in the correct basis.
        
        # If we didn't rotate back for X-basis code, we are currently in Z-basis.
        # Measuring in Z-basis is effectively Measuring in X-basis of the original state.
        # So for X-basis code:
        #   - We rotated Data H->Z basis.
        #   - We measured Z-parity (which is X-parity of original).
        #   - Now we want to measure Data in X-basis. 
        #   - Since Data is currently in Z-basis (due to H), measuring in Z (M) IS measuring in X of original.
        # So we don't need to do anything for X-basis if we want to measure final logical state.
        
        # However, strictly for the circuit to be "state restoration" we should H back.
        # But here we just want to measure.
        
        # Let's handle the measurement explicitly to be clear.
        if self.basis == 'x':
             # We are currently in Z-basis (rotated). To measure X-basis of the *code*, we just measure Z.
             # Wait, logic check:
             # State |+++>. H -> |000>. Noise Z -> X. Parity check (CNOT) checks Z-parity (X-parity of original).
             # Final measure: We want to see if it's + or -.
             # |+> -> H -> |0>. Measure 0.
             # So yes, simpler to just leave it in Z-basis and Measure Z.
             pass
        
        # Final measurement of all data qubits
        # For 'z' basis: Measure in Z.
        # For 'x' basis: We rotated to Z basis for syndrome, so Measure in Z.
        for i in range(self.num_qubits):
            circuit.append("M", [i])
        
        return circuit
    
    def create_full_circuit(self, noise_prob=0.0, measurement_noise=0.0):
        """
        Create a complete circuit for error correction simulation.
        
        Args:
            noise_prob (float): Probability of error
            measurement_noise (float): Probability of measurement error
            
        Returns:
            stim.Circuit: Complete circuit with noise and measurements
        """
        return self.create_syndrome_measurement_circuit(noise_prob, measurement_noise)
    
    def get_num_measurements(self):
        """
        Get the total number of measurements in the circuit.
        
        Returns:
            int: Number of syndrome measurements + data qubit measurements
        """
        return self.num_ancillas + self.num_qubits


class UnprotectedQubit:
    """
    Simulates an unprotected qubit for comparison with error-corrected qubits.
    """
    
    def __init__(self, basis='z'):
        """
        Initialize an unprotected qubit.
        
        Args:
            basis (str): 'z' for bit-flip (X noise), 'x' for phase-flip (Z noise)
        """
        self.num_qubits = 1
        self.basis = basis
    
    def create_circuit(self, noise_prob=0.0):
        """
        Create a simple circuit with a single qubit and noise.
        
        Args:
            noise_prob (float): Probability of error
            
        Returns:
            stim.Circuit: Simple circuit with one qubit
        """
        circuit = stim.Circuit()
        
        # Single qubit initialized to |0⟩
        if self.basis == 'x':
            circuit.append("H", [0])
            
        # Add noise
        noise_op = "X_ERROR" if self.basis == 'z' else "Z_ERROR"
        if noise_prob > 0:
            circuit.append(noise_op, [0], noise_prob)
        
        # Measure the qubit
        if self.basis == 'x':
            circuit.append("H", [0])
            
        circuit.append("M", [0])
        
        return circuit


def create_repetition_code(code_distance, basis='z'):
    """
    Factory function to create a repetition code.
    
    Args:
        code_distance (int): Number of physical qubits (3, 5, or 7)
        basis (str): 'z' for bit-flip, 'x' for phase-flip
        
    Returns:
        RepetitionCode: Initialized repetition code
    """
    return RepetitionCode(code_distance, basis)
