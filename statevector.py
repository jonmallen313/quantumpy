import numpy as np

class StateVector:
	#initialize a state vector
	def __init__(self, num_qubits):
	
		#store how many qubits we want to track
		self.n = num_qubits
	
		#each extra qubit doubles the array size, total size of the internal
		#array = 2^n
		self.dim = 2 ** num_qubits

		self.state = np.zeros(self.dim, dtype=complex)

		#setfirst element to 1
		self.state[0] = 1.0
	
	#rescale the array so the magnitude = 1 to prevent drifting 
	def normalize(self):
	
		# compute the array length using euclidean norm
		norm = np.linalg.norm(self.state)

		#avoid division by zero if something went wrong
		if norm == 0:
			raise ValueError("Cannot normalize a zero-length vector")

		#divide every element by the norm to keep size stable
		self.state = self.state / norm

	
	#controls how the object prints when you run print(obj)	
	def __repr__(self):
		return f"StateVector(n={self.n}, state={selfe.state})"

		
	#multiply the internal vector by a matrix.
	#the gate size must match the vector size.
	def apply_gate(self, gate):
		#check dimensions match
		if gate.dim != self.dim:
			raise ValueError("Gate and state dimensions do not match")
		
		#matrix multiplication (core operation)
		self.state = gate.matrix @ self.state
		
		#keep vector scaled
		self.normalize()

def pretty_print(state):
    dim = len(state)                 # length of the state vector
    bits = int(np.log2(dim))         # number of qubits

    for i, amp in enumerate(state):
        bitstring = format(i, f'0{bits}b')      # binary string of qubit state
        prob = abs(amp)**2                       # probability = |amplitude|^2
        print(f"|{bitstring}> : amplitude = {amp}, probability = {prob:.3f}")
