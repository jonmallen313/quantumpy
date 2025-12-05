from ..quantum_circuit import QuantumCircuit, H

qc = QuantumCircuit(3)
qc.apply_gate(H, 0)
qc.apply_gate(H, 1)

print("State before measurement:")
qc.print_state()

result = qc.measure_qubits([0, 2]) #measure LSB and MSB
print("Measured qubits (0,2):", result)

print("State after measurement:")
qc.print_state()
