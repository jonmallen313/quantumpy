import numpy as np

class Gate:
	def __init__(self, matrix):
		#store a transformation matrix
		
		# convert input to numpy array for consistent operations
		self.matrix = np.array(matrix, dtype=complex)

		#store dimension
		self.dim = self.matrix.shape[0]

	def __repr__(self):
		#control how object prints when using print(obj)
		return f"Gate(dim={self.dim}, matrix=\n{self.matrix})"

H = Gate((1/np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex))
