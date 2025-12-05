# QuantumPy

A minimal Python quantum simulator with verified teleportation and multi-qubit support.  

No external frameworks. just clean linear algebra and gates applied directly to statevectors.

---

## Features

- Pure Python **n-qubit statevector simulator**  
- Supports: H, X, Z, CNOT, measurement, and amplitude extraction  
- Implements **quantum teleportation** with verified output  
- Full test suite ensures correctness for basis and superposition states  

---

## Quantum Foundations

- Qubits represented as complex vectors \(|\psi\rangle = \alpha|0\rangle + \beta|1\rangle\)  
- Multi-qubit states live in \(2^n\)-dimensional Hilbert space  
- Gates applied via unitary matrices expanded over the full system  
- Measurement collapses the state probabilistically according to quantum mechanics  

Teleportation steps implemented end-to-end:

1. Prepare input qubit  
2. Create Bell pair  
3. Alice entangles input with her half  
4. Measure qubits, send classical bits  
5. Bob applies corrections, input state restored  

---

## Usage

```bash
python3 -m quantumpy.tests.test_teleportation
python3 -m quantumpy.tests.test_bell
