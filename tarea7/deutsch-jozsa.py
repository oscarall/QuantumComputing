"""Deutsch-Jozsa algorithm on three qubits in Cirq."""

# Import the Cirq library
import cirq

# Get three qubits -- two data and one target qubit
q0, q1, q2 = cirq.LineQubit.range(3)

oracles = {
    '0': [],
    '1': [cirq.X(q2)],
    'x1': [cirq.CNOT(q0, q2)],
    'x2': [cirq.CNOT(q1, q2)],
    'notx1': [cirq.CNOT(q0, q2), cirq.X(q2)],
    'notx2': [cirq.CNOT(q1, q2), cirq.X(q2)],
    'xor': [cirq.CNOT(q0, q2), cirq.CNOT(q1, q2)],
    'notxor': [cirq.CNOT(q0, q2), cirq.CNOT(q1, q2), cirq.X(q2)]
}

def your_circuit(oracle):
    """Yields a circuit for the Deutsch-Jozsa algorithm on three qubits."""
    # phase kickback trick
    yield cirq.X(q2), cirq.H(q2)

    # equal superposition over input bits
    yield cirq.H(q0), cirq.H(q1)

    # query the function
    yield oracle

    # interference to get result, put last qubit into |1>
    yield cirq.H(q0), cirq.H(q1), cirq.H(q2)

    # a final OR gate to put result in final qubit
    yield cirq.X(q0), cirq.X(q1), cirq.CCX(q0, q1, q2)
    yield cirq.measure(q2)

# Get a simulator
simulator = cirq.Simulator()

# Execute circuit for oracles
for tag, oracle in oracles.items():
    print("____________________________________________________________________________________________________\n")
    print(f"\t{tag}\n")
    print("circuit: \n")
    circuit = cirq.Circuit(your_circuit(oracle))
    print(circuit)
    result = simulator.run(circuit, repetitions=10)
    print("\nresult:\n")
    print(result)