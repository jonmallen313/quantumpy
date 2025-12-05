from ..quantum_circuit import QuantumCircuit, H, X

qc = QuantumCircuit(3)

qc.apply_gate(H, 0)
qc.apply_gate(H, 1)
qc.apply_gate(X, 2)

print("State before measurement:")
qc.print_state()

result = qc.measure_all()
print("\nMeasured bitstring:", result)

print("\nState after measurement:")
qc.print_state()
