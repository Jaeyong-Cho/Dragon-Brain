# Quantum Computing

Quantum computing leverages quantum mechanics to solve complex problems beyond classical computers.

## Quantum Mechanics Basics

### Superposition

A quantum bit (qubit) can exist in **multiple states simultaneously**.

Unlike classical bits (0 or 1), qubits can be:
- |0⟩
- |1⟩
- **Superposition** of both: α|0⟩ + β|1⟩

### Entanglement

Two or more qubits become **correlated** in ways classical systems cannot:

- Measuring one qubit instantly affects others
- Einstein's "spooky action at a distance"
- Key resource for quantum algorithms

### Quantum Interference

Amplify correct answers and cancel wrong ones:

- Constructive interference
- Destructive interference
- Enables quantum speedup

## Qubits

### Physical Implementations

- **Superconducting Qubits**: IBM, Google
- **Trapped Ions**: IonQ, Honeywell
- **Photonic Qubits**: Light-based
- **Topological Qubits**: Microsoft's approach
- **Neutral Atoms**: Atom Computing

### Qubit Properties

- **Coherence Time**: How long quantum state lasts
- **Gate Fidelity**: Accuracy of operations
- **Connectivity**: Which qubits can interact

## Quantum Gates

Quantum operations analogous to classical logic gates:

### Single-Qubit Gates

- **Pauli X**: Quantum NOT gate
- **Pauli Y, Z**: Phase rotations
- **Hadamard (H)**: Creates superposition
- **Phase Gates**: T, S gates

### Multi-Qubit Gates

- **CNOT**: Controlled-NOT gate
- **Toffoli**: Controlled-controlled-NOT
- **SWAP**: Exchange qubit states

## Quantum Algorithms

### Shor's Algorithm

Factor large numbers exponentially faster:

- **Breaks RSA encryption**
- Polynomial time on quantum computer
- Exponential time on classical computer

### Grover's Algorithm

Search unsorted database with **quadratic speedup**:

- Classical: O(N)
- Quantum: O(√N)
- Useful for optimization problems

### Quantum Fourier Transform

Foundation for many quantum algorithms:

- Period finding
- Phase estimation
- **Quantum advantage**

### Variational Quantum Eigensolver (VQE)

Hybrid quantum-classical algorithm:

- Quantum chemistry
- Material science
- Drug discovery

## Quantum Programming

### Qiskit (IBM)

Python-based quantum programming:

```python
from qiskit import QuantumCircuit, execute, Aer

# Create circuit
qc = QuantumCircuit(2, 2)
qc.h(0)  # Hadamard gate
qc.cx(0, 1)  # CNOT gate
qc.measure([0, 1], [0, 1])

# Execute
backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend, shots=1000)
result = job.result()
```

### Other Frameworks

- **Cirq**: Google's framework
- **Q#**: Microsoft's language
- **Pennylane**: Quantum machine learning
- **Forest**: Rigetti's platform

## Quantum Error Correction

Qubits are **fragile and error-prone**:

### Challenges

- Decoherence
- Gate errors
- Measurement errors
- Environmental noise

### Solutions

- **Quantum Error Correction Codes**: Shor code, Surface code
- **Fault-Tolerant Quantum Computing**
- Multiple physical qubits per logical qubit

## Quantum Advantage

### NISQ Era

**Noisy Intermediate-Scale Quantum**:

- 50-1000 qubits
- Limited error correction
- Exploring applications
- Hybrid algorithms

### Applications

- **Cryptography**: Quantum key distribution
- **Optimization**: Logistics, finance
- **Drug Discovery**: Molecular simulation
- **Materials Science**: New materials
- **Machine Learning**: Quantum ML

## Quantum Cryptography

### Quantum Key Distribution (QKD)

Secure communication using quantum properties:

- **BB84 Protocol**: Most famous
- Eavesdropping detection
- Unconditional security

### Post-Quantum Cryptography

Classical algorithms resistant to quantum attacks:

- Lattice-based cryptography
- Code-based cryptography
- **NIST standardization**

## Major Players

### Tech Companies

- **IBM**: Cloud quantum computing
- **Google**: Quantum supremacy claim
- **Microsoft**: Topological qubits
- **Amazon**: Braket platform
- **Honeywell/Quantinuum**: Trapped ions

### Startups

- IonQ
- Rigetti Computing
- D-Wave: Quantum annealing
- Xanadu: Photonic

## Challenges

- **Scalability**: Building more qubits
- **Error Rates**: Improving fidelity
- **Temperature**: Ultra-cold requirements
- **Cost**: Expensive infrastructure
- **Talent**: Need quantum expertise

## Future Outlook

- Quantum internet
- **Universal quantum computers**
- Quantum sensors
- Integration with AI
- Transformative impact on science
