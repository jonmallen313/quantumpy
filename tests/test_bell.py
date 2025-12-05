from ..quantum_circuit import QuantumCircuit, H
import math
from collections import Counter

def approx_equal(a, b, eps=1e-8):
    return abs(a - b) < eps

def test_bell_state(verbose=False):
    qc = QuantumCircuit(2)

    # Prepare Bell: H on qubit 0, CNOT 0->1
    qc.apply_gate(H, 0)
    qc.cnot(0, 1)

    if verbose:
        print("State after preparing Bell pair (non-zero entries):")
        qc.print_state()
        print()

    # Check amplitudes at indices 0 (|00>) and 3 (|11>)
    amp00 = qc.state[0]
    amp11 = qc.state[3]
    other_sum = sum(abs(qc.state[i]) for i in range(len(qc.state)) if i not in (0, 3))

    expected_val = 1 / math.sqrt(2)
    all_pass = True

    print("=== Amplitude checks ===")
    if approx_equal(abs(amp00), expected_val):
        print(f"[PASS] |00> amplitude ≈ {expected_val:.6f}")
    else:
        print(f"[FAIL] |00> amplitude = {amp00}, expected ≈ {expected_val:.6f}")
        all_pass = False

    if approx_equal(abs(amp11), expected_val):
        print(f"[PASS] |11> amplitude ≈ {expected_val:.6f}")
    else:
        print(f"[FAIL] |11> amplitude = {amp11}, expected ≈ {expected_val:.6f}")
        all_pass = False

    if approx_equal(other_sum, 0.0, eps=1e-6):
        print("[PASS] No other basis states present")
    else:
        print(f"[FAIL] Unexpected amplitude mass on other states: {other_sum}")
        all_pass = False

    # Sampling check (recreate circuit each trial and use measure_all())
    print("\n=== Measurement correlation test (200 trials) ===")
    counts = Counter()
    trials = 200
    for _ in range(trials):
        qc2 = QuantumCircuit(2)
        qc2.apply_gate(H, 0)
        qc2.cnot(0, 1)
        outcome = qc2.measure_all()   # returns bitstring like '01' (q1q0 with q0 rightmost)
        counts[outcome] += 1

    for k in sorted(counts.keys()):
        print(f"  {k} : {counts[k]} ({counts[k]/trials:.3f})")

    if set(counts.keys()) <= {"00", "11"}:
        print("[PASS] Only '00' and '11' observed")
    else:
        print(f"[FAIL] Unexpected outcomes: {set(counts.keys())}")
        all_pass = False

    print("\n=== FINAL RESULT ===")
    if all_pass:
        print("✔ Bell test: SUCCESS — simulator behaving correctly")
    else:
        print("✘ Bell test: FAILURE — check simulator/gates")

if __name__ == "__main__":
    test_bell_state(verbose=True)
