from ..quantum_circuit import QuantumCircuit, H

qc = QuantumCircuit(1)

qc.apply_gate(H, 0) # qubit in superposition

print("State before measurement:")
qc.print_state()

result = qc.measure(0)
print("\nMeasurement result:", result)

print("\nState after measurement:")
qc.print_state()
