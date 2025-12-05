# teleportation.py
import numpy as np
from math import sqrt
from .quantum_circuit import QuantumCircuit, H, X, Z

def prepare_input_state(qc, label):
    """
    Prepare a single-qubit state on qubit 0 using gates so everything
    flows through your gate machinery (avoids direct statevector set).
    label: one of "|0>", "|1>", "|+>", "|->"
    """
    # start from |000> (default)
    if label == "|0>":
        pass  # nothing to do
    elif label == "|1>":
        qc.apply_gate(X, 0)
    elif label == "|+>":
        qc.apply_gate(H, 0)
    elif label == "|->":
        qc.apply_gate(X, 0)
        qc.apply_gate(H, 0)
    else:
        raise ValueError("Unknown label for prepare_input_state")

def teleport(qc, debug=False):
    """
    Perform teleportation on a QuantumCircuit qc of size 3.
    Assumes the input state to teleport is on qubit 0 (prepared already).
    Returns (qc_after, m0, m1)
    """
    # Step 1: create entanglement between qubit 1 (Alice) and 2 (Bob)
    qc.apply_gate(H, 1)
    qc.cnot(1, 2)
    if debug:
        print("After entangling q1-q2:")
        qc.print_state()

    # Step 2: Alice entangles her qubit (q0) with her half (q1)
    qc.cnot(0, 1)
    qc.apply_gate(H, 0)
    if debug:
        print("After Alice operations (CNOT 0->1, H on 0):")
        qc.print_state()

    # Step 3: Alice measures q0 and q1 (these collapse the state)
    m0 = qc.measure(0)  # measurement of qubit 0
    m1 = qc.measure(1)  # measurement of qubit 1
    if debug:
        print(f"Alice measurements: m0={m0}, m1={m1}")
        print("After measurements (collapsed):")
        qc.print_state()

    # Step 4: Classical corrections on Bob's qubit (q2)
    if m1 == 1:
        qc.apply_gate(X, 2)
    if m0 == 1:
        qc.apply_gate(Z, 2)
    if debug:
        print("After Bob corrections:")
        qc.print_state()

    return qc, m0, m1

def extract_qubit_state(qc, qubit_index, measured=None):
    """
    Extract single-qubit amplitudes (alpha, beta) for `qubit_index`,
    conditioned on the values of the other qubits.

    Args:
      qc: QuantumCircuit after collapse(s)
      qubit_index: index of the qubit to extract (LSB-first)
      measured: optional dict {qubit_index: bit_value} of classical results.
                If None, the function will infer the fixed values of other qubits
                by finding the set of basis indices with non-negligible amplitude.

    Returns:
      (alpha, beta) normalized complex amplitudes for the target qubit.
    """
    n = qc.n
    size = 2**n

    if measured is None:
        # infer measured values by looking at which basis indices have amplitude
        nonzero = [i for i in range(size) if abs(qc.state[i]) > 1e-12]
        if not nonzero:
            return 0+0j, 0+0j
        # check other-qubit bits are consistent across nonzero indices
        measured = {}
        for q in range(n):
            if q == qubit_index:
                continue
            bits = {(idx >> q) & 1 for idx in nonzero}
            if len(bits) == 1:
                measured[q] = bits.pop()
            else:
                # other qubits are not fixed — can't extract clean single-qubit state
                # fallback: trace out other qubits (compute reduced density vector amplitudes)
                # Here we compute alpha,beta by summing amplitudes over other qubits.
                alpha = 0+0j
                beta = 0+0j
                for idx in range(size):
                    bit = (idx >> qubit_index) & 1
                    if bit == 0:
                        alpha += qc.state[idx]
                    else:
                        beta += qc.state[idx]
                norm = (abs(alpha)**2 + abs(beta)**2)**0.5
                if norm != 0:
                    return alpha / norm, beta / norm
                return 0+0j, 0+0j

    # Now we have a measured dict describing fixed values for other qubits.
    alpha = 0+0j
    beta  = 0+0j
    for idx in range(size):
        ok = True
        for q, val in measured.items():
            if ((idx >> q) & 1) != val:
                ok = False
                break
        if not ok:
            continue
        bit = (idx >> qubit_index) & 1
        if bit == 0:
            alpha += qc.state[idx]
        else:
            beta += qc.state[idx]

    # normalize
    norm = (abs(alpha)**2 + abs(beta)**2)**0.5
    if norm != 0:
        alpha /= norm
        beta  /= norm
    return alpha, beta

