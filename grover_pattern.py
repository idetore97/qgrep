import matplotlib
from qiskit import Aer, execute
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.tools.visualization import plot_histogram
from qiskit.providers.aer import noise
import numpy as np
import matplotlib.pyplot as plt

def grover_circuit(n,o,iter):
    """Grover Search Algorithm
    
    :param n: Number of qubits (not including ancilla)
    :param o: Oracle int to find 

    :return qc: Qiskit circuit
    """
    def apply_hadamard(qc, qubits,a=None) -> None:
        """Apply a H-gate to 'qubits' in qc"""
        for q in qubits:
            qc.h(q)
        if a is not None:
            qc.h(a)

    def initialize_bits(qc,qubits,a) -> None:
        "Start qubits at 0 and ancilla bit at 1"
        for q in qubits:
            qc.reset(q)

        qc.reset(a[0])
        qc.x(a[0])

    def apply_mean_circuit(qc, qubits) -> None:
        """Apply a H-gate to 'qubits' in qc"""
        control_qubits = []
        for q in qubits:
            qc.h(q)
            qc.x(q)

            control_qubits.append(q)
    
        cZ = control_qubits[-1]
        control_qubits.pop()

        qc.h(cZ)
        qc.mcx(control_qubits,cZ)
        qc.h(cZ)

        for q in qubits:
            qc.x(q)
            qc.h(q)

    def create_oracle(qc,qubit,ancilla,oracle,n) -> None:
        """Creates a quantum oracle."""
        test_list = []
        for q in qubit:
            test_list.append(q)

        _oracle_logic(qc, qubit, oracle,n)

        qc.mcx(test_list,ancilla[0])

        _oracle_logic(qc, qubit, oracle,n)

    def _oracle_logic(qc, qubit, oracle,n) -> None:
        if 0 <= oracle <= 2**len(qubit)-1:
            bin_list = [int(i) for i in list('{0:0b}'.format(oracle))]

            if len(bin_list) < n:
                for _ in range(0,n-len(bin_list)):
                    bin_list.insert(0,0)

            for i in range(0,len(bin_list)):
                if bin_list[i] == 0:
                    qc.x(q[i])

        else:
            raise ValueError('Oracle must be between 0 and 2^n-1')

#    print(f"Creating circuit with {n} qubits")
    q = QuantumRegister(n, 'q')
    a = QuantumRegister(1, 'a')
    c = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(q,a,c)

    i2b = "{0:b}".format(o)
#    print(f"Oracle set to: {o} ({i2b})")
#    print(" ")
    initialize_bits(qc,q,a)
    qc.barrier(q,a)
    apply_hadamard(qc,q,a)
#    print(f"Generating {iter} Grover module(s)")
#    print("=====================================")
    for _ in range(1,iter+1):
        qc.barrier(q,a)
        create_oracle(qc,q,a,o,n)

        qc.barrier(q,a)

        apply_mean_circuit(qc, q)

        qc.barrier(q,a)

    for i in range(0,len(q)):
        qc.measure(q[i],c[len(q)-1-i])
    
    return qc

def bypass_draw(qc,bypass=True) -> None:
    if bypass is False:
        return qc.draw(output="mpl")

def simulate_results(qc,show_hist=True):
    backend = Aer.get_backend('qasm_simulator')
    job = execute(qc, backend, shots=1024)
    result = job.result()
    counts = result.get_counts()

    total = sum(counts.values())
    max_key = (max(counts, key=counts.get))

    match_rate = counts[max_key]/total
#    print(f"Highest match: {str(max_key).lstrip('0')}")
#    print(f"Probability: {match_rate}")
#    print(f"Runtime: {round(result.time_taken,4)} s")

    if show_hist is True:
        return plot_histogram(counts)
    else:
        return counts

def match_ints(arr, qc):
    """
    Function to glue quantum circuit code to unicode encodings of text

    :param arr: Array of unicode values
    :param qc: Quantum circuit

    :return probs: Array of match probabilities
    """
    # Get counts per Unicode and convert to probabilities
    counts = simulate_results(qc, show_hist=False).int_outcomes()
    keys = list(counts.keys())
    keys.sort()
    probs = np.zeros(len(arr))
    for i, target in enumerate(arr):
        try:
            probs[i] = counts[target]
        except:
            probs[i] = 0
    probs = probs / sum(probs)
    return probs
