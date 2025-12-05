from ..statevector import StateVector
from ..gate import Gate
import numpy as np

# make a 1-qubit state (size 2)
s = StateVector(1)

#create a 2x2 matrix to transofrm it
test_matrix = np.array([[0,1],[1,0]], dtype=complex)

g = Gate(test_matrix)

#apply the gate
s.apply_gate(g)

print("New state:", s.state)
