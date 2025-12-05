from .quantum_circuit import QuantumCircuit, H

def prepare_bell(qc):
	#prepare a bell pair between qubit 0 and qubit 1. Mutates qc in place.
	qc.apply_gate(H,0)
	qc.cnot(0, 1)
	return qc

def is_bell_state(qc, tol=1e-8):
	# quick check whether the current 2 qubit state in qc is a bell pair
	# returns True/False.
	if qc.n < 2:
		return False

	size = 2**qc.n
	amps = qc.state
	
	# find noneligible indicies
	nonzero = [(i, amps[i]) for i in range(size) if abs(amps[i]) > tol]

	if len(nonzero) != 2:
		return False

	idxs = sorted([i for i, _ in nonzero])
	if idxs != [0, 3]:
		return False

	amp0 = amps[0]
	amp3 = amps[3]

	#check equal magnitude
	return abs(abs(amp0) - abs(amp3)) < tol
