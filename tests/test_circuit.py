from ..quantum_circuit import QuantumCircuit, H, X, Z

qc = QuantumCircuit(3)

qc.apply_gate(H, 0)
qc.apply_gate(H, 1)
qc.apply_gate(X, 2)

qc.print_state()
