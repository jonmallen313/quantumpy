from ..quantum_circuit import QuantumCircuit, H

qc = QuantumCircuit(2)

#put qubit 0 into superposition
qc.apply_gate(H, 0) 
# entangle: |00> + |11>
qc.cnot(0, 1)

qc.print_state()
