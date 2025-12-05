from math import sqrt
from quantumpy.quantum_circuit import QuantumCircuit
from quantumpy.teleportation import prepare_input_state, teleport, extract_qubit_state

def expected_amplitudes(label):
    """Return (alpha, beta) for the input labels."""
    if label == "|0>":
        return (1+0j, 0+0j)
    if label == "|1>":
        return (0+0j, 1+0j)
    if label == "|+>":
        x = 1 / sqrt(2)
        return (x+0j, x+0j)
    if label == "|->":
        x = 1 / sqrt(2)
        return (x+0j, -x+0j)
    raise ValueError("Unknown label")

def run_case(label, verbose=True):
    print(f"\n---- Testing teleportation of input state: {label} ----")

    qc = QuantumCircuit(3)

    # prepare input state on qubit 0
    prepare_input_state(qc, label)

    if verbose:
        print("State BEFORE teleport (non-zero entries):")
        qc.print_state()

    # perform teleportation
    qc_after, m0, m1 = teleport(qc, debug=verbose)

    # extract Bob’s qubit (qubit 2)
    alpha, beta = extract_qubit_state(qc_after, 2)

    # expected values
    exp_alpha, exp_beta = expected_amplitudes(label)

    # compare
    ok = (
        abs(alpha - exp_alpha) < 1e-6 and
        abs(beta - exp_beta) < 1e-6
    )

    print(f"\nExtracted final Bob qubit:")
    print(f"  alpha = {alpha}")
    print(f"  beta  = {beta}")
    print("Expected:")
    print(f"  alpha = {exp_alpha}")
    print(f"  beta  = {exp_beta}")

    if ok:
        print(f"[PASS] Teleportation correct for {label}")
    else:
        print(f"[FAIL] Teleportation incorrect for {label}")

    return ok

if __name__ == "__main__":
    tests = ["|0>", "|1>", "|+>", "|->"]
    all_ok = True
    for t in tests:
        if not run_case(t, verbose=False):
            all_ok = False

    print("\n===============================")
    if all_ok:
        print("✔ ALL TELEPORTATION TESTS PASSED")
    else:
        print("✘ SOME TELEPORTATION TESTS FAILED")
