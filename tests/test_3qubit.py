from ..statevector import StateVector, pretty_print
from ..gate import Gate, H
import numpy as np

sv = StateVector(3)

#expand h to 3 qubits (apply to qubit 0)
def expand_gate(single_gate, target_qubit, n_qubits):
	result = 1
	for i in range(n_qubits):
		if i == target_qubit:
			result = np.kron(result, single_gate.matrix)
		else:
			result = np.kron(result, np.eye(2, dtype= complex))
	return result

H1 = expand_gate(H, target_qubit=0, n_qubits=3)

sv.apply_gate(Gate(H1))


pretty_print(sv.state)
