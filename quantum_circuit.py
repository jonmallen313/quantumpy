import numpy as np
from math import sqrt

#basic gate matrices
H = (1/sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

class QuantumCircuit:
	def __init__(self, num_qubits):
		self.n = num_qubits
		self.state = np.zeros(2**num_qubits, dtype=complex)
		self.state[0] = 1.0

	def apply_gate(self, gate, target):
		#apply a single qubit gate with LSB first convention
		full_gate = 1
		for i in range(self.n):
			if i == target:
				full_gate = np.kron(gate, full_gate)
			else:
				full_gate = np.kron(np.eye(2), full_gate)
		self.state = full_gate @ self.state

	def apply_controlled(self, gate, control, target):
		#apply controlled gate
		size = 2**self.n
		new_state = np.zeros(size, dtype=complex)
		
		for basis in range(size):
			if (basis >> control) & 1:
				bit = (basis >> target) & 1
				flipped = basis ^ (1 << target)
				if bit == 0:
					new_state[flipped] += gate[0][1] * self.state[basis]
					new_state[basis] += gate[0][0] * self.state[basis]
				else:
					new_state[flipped] += gate[1][0] * self.state[basis]
					new_state[basis] += gate[1][1] * self.state[basis]
			else:
				new_state[basis] += self.state[basis]

		self.state = new_state
	
	def cnot(self, control, target):
		#apply a controlled x gate
		size = 2**self.n
		new_state = np.zeros(size, dtype=complex)
		
		for basis in range(size):
			amp = self.state[basis]
		
			ctrl_bit = (basis >> control) & 1
			tgt_bit = (basis >> target) & 1

			if ctrl_bit == 1:
			#flip target bit
				flipped = basis ^ (1 << target)
				new_state[flipped] += amp
			else:
				new_state[basis] += amp
		self.state = new_state

	def measure(self, qubit):
		#measure a single qubit and collapse the full state. returns classic bit 0 or 1
		size = 2**self.n
		
		# Probabilities for outcomes 0 and 1
		prob0 = 0.0
		prob1 = 0.0

		for basis in range(size):
			amp = self.state[basis]
			bit = (basis >> qubit) & 1
			
			if bit == 0:
				prob0 += abs(amp)**2
			else:
				prob1 += abs(amp)**2

		# normalize floating point errors
		total = prob0 + prob1
		if total == 0:
			raise RuntimeError("Invalid state normalization.")
		prob0 /= total
		prob1 /= total

		#sample outcome
		outcome = 1 if np.random.rand() < prob1 else 0

		#collapse the state: keep only amplitudes consistent with outcome
		new_state = np.zeros(size, dtype=complex)

		for basis in range(size):
			bits = (basis >> qubit) & 1
			if bits == outcome:
				new_state[basis] = self.state[basis]

		# Renormalize the collapsed state
		norm = np.sqrt(np.sum(np.abs(new_state)**2))
		if norm < 1e-15:
			#find the surviving amplitude and normalize it
			for i in range(size):
				if abs(new_state[i]) > 1e-15:
					new_state[:] = 0
					new_state[i] = 1.0 + 0j
					break
		else:
			new_state /= norm

		self.state = new_state
		return outcome
		
		
	def measure_all(self):
	#measure all qubits and collapse the entire state.
	#returns bitstring like '0101'
		size = 2**self.n
		# compute probability of each basis state
		probs = np.abs(self.state)**2
		
		outcome_index = np.random.choice(size, p=probs)
		
		bitstring = f"{outcome_index:0{self.n}b}"

		#collapse: keep only the sampled basis state
		new_state = np.zeros(size, dtype=complex)
		new_state[outcome_index] = 1.0

		self.state = new_state

		return bitstring

	def measure_qubits(self, qubits):
		#measure a subset of qubits. 'qubits' = list of qubit indicies
		#returns a bitstring of the measured qubits
		
		size = 2**self.n
		#compute probabilities of each basis state
		probs = np.abs(self.state)**2

		outcome_index = np.random.choice(size, p=probs)

		full_bitstring = f"{outcome_index:0{self.n}b}"

		measured = ''.join(full_bitstring[self.n - 1 - q] for q in qubits)
		
		#collapse like measure_all
		new_state = np.zeros(size, dtype=complex)
		new_state[outcome_index] = 1.0
		self.state = new_state

		return measured

	def print_state(self):
		for i, amp in enumerate(self.state):
			if abs(amp) > 1e-15:
				print(f"|{i:0{self.n}b}> : amplitude = {amp}")
