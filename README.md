# A classical (non-quantum) implementation of the (quantum) Grover's algorithm

This is a classical (non-quantum) algorithm of the (quantum) Grover's algorithm. The Grover's algorithm (https://en.wikipedia.org/wiki/Grover%27s_algorithm) is a an algorithm that, with high probability, identifies a solution to a black box function.

## Introduction
For a black box function `f(x)` with `N` potential solutions `x`, among which `k` are correct, the Grover's algorithm can, with high probability, identify the one of the correct solutions `k` in order `sqrt(N)`. This is significant speedup compared to the order `N` steps required by the classical approach, which involves checking all potential solutions.

## Classical representation of the quantum states and operations
This implementation is classical -- it runs on a classical computer. It therefore has to simulate the quantum operations that would normally be applied. For the `N` potential solutions, we can use `N_q = ceil(log_2(N))` qubits, which are specified by `2^(N_q)` complex numbers (minus the normalization).

### A classical representation a quantum state
I represent the `N_qubit` quantum state as a *vector* of `2^N_qubit` complex numbers whose magnitudes sum to 1 (probability normalization) (https://en.wikipedia.org/wiki/Quantum_state).

### A unitary operator
A unitary operator, which changes the quantum state in a valid way, can be represented as a unitary `2^N_qubit x 2^N_qubit` matrix (https://en.wikipedia.org/wiki/Operator_(physics)#Operators_in_quantum_mechanics). To evolve the quantum state represented as a vector, you can matrix-multiply it with the corresponding matrix.




