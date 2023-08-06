"""
The operators module contains the Operator class, instances of which
represent Operators on vector spaces for multi-qubit systems, and
factory functions for creating specific operators.

Each of the factory functions (but not the Operator class) is aliased
at the top-level module, so that, for example, one can call
``qcircuits.Hadamard()`` instead of ``qcircuits.state.Hadamard()``.
"""


from itertools import product

import numpy as np

from qcircuits.tensors import Tensor


class Operator(Tensor):
    """
    A container class for a tensor representing an operator on a vector
    space for a quantum system, and associated methods.

    Parameters
    ----------
    tensor : numpy complex128 multidimensional array
        The tensor representing the operator.
    """

    def __init__(self, tensor):
        super().__init__(tensor)
        # TODO check unitary

    def __repr__(self):
        return 'Operator for {}-rank state space.'.format(self.rank // 2)

    def __str__(self):
        s = self.__repr__() + ' Tensor:\n'
        s += super().__str__()
        return s


    @property
    def adj(self):
        """
        Get the adjoint/inverse of this operator,
        :math:`A^{\dagger} = (A^{*})^{T}`. As the operator is unitary,
        :math:`A A^{\dagger} = I`.

        Returns
        -------
        Operator
            The adjoint operator.
        """

        d = self.rank
        permutation = [0] * d
        permutation[::2] = range(1, d, 2)
        permutation[1::2] = range(0, d, 2)
        t = np.conj(self._t).transpose(permutation)
        return Operator(t)

    # Compose this operator with another operator, or apply it to a state vector
    # TODO break up this function
    def __call__(self, arg, qubit_indices=None):
        """
        Applies this Operator to another Operator, as in operator
        composition A(B), or to a :py:class:`.State`, as in A(v). This means that
        if two operators A and B will be applied to state v in sequence,
        either B(A(v)) or (B(A))(v) are valid.

        This operator may be applied to state vectors of higher rank
        if the qubits to which it is to be applied are specified in the
        `qubit_indices` parameter.

        Parameters
        ----------
        arg : State or Operator
            The state that the operator is applied to, or the operator
            with which the operator is composed.
        qubit_indices: list of int
            If the operator is applied to a state vector for a larger
            quantum system, the user must supply a list of the indices
            of the qubits to which the operator is to be applied.
            These can also be used to apply the operator to the qubits
            in arbitrary order.

        Returns
        -------
        State or Operator
            The state vector or operator resulting in applying the
            operator to the argument.
        """

        d = arg.rank
        if qubit_indices is not None:
            qubit_indices = list(qubit_indices)

        if qubit_indices is not None:
            if len(set(qubit_indices)) != len(qubit_indices):
                raise ValueError('Qubit indices list contains repeated elements.')

        # If we're applying to another operator, the ranks should match
        if type(arg) is Operator:
            op_indices = range(1, self.rank, 2)
            arg_indices = range(0, d, 2)

            if len(op_indices) != len(arg_indices):
                raise ValueError('An operator can only be composed with an operator of equal rank.')
            if qubit_indices is not None:
                raise ValueError('Qubit indices should only be supplied when applying an operator to a ' \
                                 'state vector, not composing it with another operator.')

        # We can apply an operator to a larger state, as long as we specify which axes of
        # the state vector are contracted (i.e., which qubits the operator is applied to).
        else:
            op_indices = range(1, self.rank, 2)
            arg_indices = range(d)

            if len(op_indices) > len(arg_indices):
                raise ValueError('An operator for a d-rank state space can only be applied to ' \
                                 'state vectors whose rank is >= d.')
            if len(op_indices) < len(arg_indices) and qubit_indices is None:
                raise ValueError('Applying operator to too-large state vector without supplying qubit indices.')
            if qubit_indices is not None:
                if min(qubit_indices) < 0:
                    raise ValueError('Supplied qubit index < 0.')
                if max(qubit_indices) >= len(arg_indices):
                    raise ValueError('Supplied qubit index larger than state vector rank.')

                if len(qubit_indices) == len(op_indices):
                    arg_indices = [arg_indices[index] for index in qubit_indices]
                else:
                    raise ValueError('Length of qubit_indices does not match number of operator ' \
                                     'lower indices (i.e., operator rank/2).')

        result = np.tensordot(self._t, arg._t, (op_indices, arg_indices))

        # Our convention is to have lower and upper indices of operators interleaved.
        # Using tensordot on operator-operator application leaves us with all upper
        # indices followed by all lower. We transpose the result to fix this.
        if type(arg) is Operator:
            permute = [0] * d
            permute[::2] = range(d//2)
            permute[1::2] = range(d//2, d)
            result = np.transpose(result, permute)
        # Likewise, application of operators to sub-vectors using tensordot leaves
        # our indices out of order, so we transpose them back.
        # This could be avoided with einsum, but it's easier to work with tensordot.
        elif qubit_indices is not None:
            permute = list(range(len(qubit_indices), d))
            # We also need to permute the indices if the qubit_indices are
            # supplied out-of-order.
            for i, v in zip(np.argsort(qubit_indices), np.sort(qubit_indices)):
                permute.insert(v, i)
            result = np.transpose(result, permute)

        return arg.__class__(result)


# Factory functions for building operators

def Identity(d=1):
    """
    Produce the `d`-qubit identity operator :math:`I^{\\otimes d}`.

    Parameters
    ----------
    d : int
        The number of qubits described by the state vector on which
        the produced operator will act.

    Returns
    -------
    Operator
        A rank `2d` tensor describing the operator.

    See Also
    --------
    PauliX, PauliY, PauliZ, Hadamard, Phase, SqrtNot, CNOT, Toffoli
    Swap, SqrtSwap, ControlledU, U_f
    """

    return Operator(np.array([[1.0 + 0.0j, 0.0j],
                              [0.0j, 1.0 + 0.0j]])).tensor_power(d)


def PauliX(d=1):
    """
    Produce the `d`-qubit Pauli X operator :math:`X^{\\otimes d}`,
    or `not` gate.
    Maps: \|0⟩ -> \|1⟩, \|1⟩ -> \|0⟩.

    Parameters
    ----------
    d : int
        The number of qubits described by the state vector on which
        the produced operator will act.

    Returns
    -------
    Operator
        A rank `2d` tensor describing the operator.

    See Also
    --------
    Identity, PauliY, PauliZ, Hadamard, Phase, SqrtNot, CNOT, Toffoli
    Swap, SqrtSwap, ControlledU, U_f
    """

    return Operator(np.array([[0.0j, 1.0 + 0.0j],
                              [1.0 + 0.0j, 0.0j]])).tensor_power(d)


def PauliY(d=1):
    """
    Produce the `d`-qubit Pauli Y operator :math:`Y^{\\otimes d}`.
    Maps: \|0⟩ -> `i` \|1⟩, \|1⟩ -> -`i` \|0⟩.

    Parameters
    ----------
    d : int
        The number of qubits described by the state vector on which
        the produced operator will act.

    Returns
    -------
    Operator
        A rank `2d` tensor describing the operator.

    See Also
    --------
    Identity, PauliX, PauliZ, Hadamard, Phase, SqrtNot, CNOT, Toffoli
    Swap, SqrtSwap, ControlledU, U_f
    """

    return Operator(np.array([[0.0j, -1.0j],
                              [1.0j, 0.0j]])).tensor_power(d)


def PauliZ(d=1):
    """
    Produce the `d`-qubit Pauli Z operator :math:`Z^{\\otimes d}`,
    or phase inverter.
    Maps: \|0⟩ -> \|0⟩, \|1⟩ -> -\|1⟩.

    Parameters
    ----------
    d : int
        The number of qubits described by the state vector on which
        the produced operator will act.

    Returns
    -------
    Operator
        A rank `2d` tensor describing the operator.

    See Also
    --------
    Identity, PauliX, PauliY, Hadamard, Phase, SqrtNot, CNOT, Toffoli
    Swap, SqrtSwap, ControlledU, U_f
    """
    return Operator(np.array([[1.0 + 0.0j, 0.0j],
                              [0.0j, -1.0 + 0.0j]])).tensor_power(d)


def Hadamard(d=1):
    """
    Produce the `d`-qubit Hadamard operator :math:`H^{\\otimes d}`.
    Maps: \|0⟩ -> :math:`\\frac{1}{\\sqrt{2}}` (\|0⟩+\|1⟩) = \|+⟩,
    \|1⟩ -> :math:`\\frac{1}{\\sqrt{2}}` (\|0⟩-\|1⟩) = \|-⟩.

    Parameters
    ----------
    d : int
        The number of qubits described by the state vector on which
        the produced operator will act.

    Returns
    -------
    Operator
        A rank `2d` tensor describing the operator.

    See Also
    --------
    Identity, PauliX, PauliY, PauliZ, Phase, SqrtNot, CNOT, Toffoli
    Swap, SqrtSwap, ControlledU, U_f
    """
    return Operator(1/np.sqrt(2) *
        np.array([[1.0 + 0.0j,  1.0 + 0.0j],
                  [1.0 + 0.0j, -1.0 + 0.0j]])).tensor_power(d)


def Phase(phi=np.pi/2, d=1):
    """
    Produce the `d`-qubit Phase change operator.
    Maps: \|0⟩ -> \|0⟩, \|1⟩ -> :math:`e^{i\phi}` \|1⟩.

    Parameters
    ----------
    d : int
        The number of qubits described by the state vector on which
        the produced operator will act.

    Returns
    -------
    Operator
        A rank `2d` tensor describing the operator.

    See Also
    --------
    Identity, PauliX, PauliY, PauliZ, Hadamard, SqrtNot, CNOT, Toffoli
    Swap, SqrtSwap, ControlledU, U_f
    """

    return Operator(np.array([[1.0 + 0.0j, 0.0j],
                              [0.0j, np.exp(phi * 1j)]])).tensor_power(d)


def SqrtNot(d=1):
    """
    Produce the `d`-qubit operator that is the square root of the
    `d`-qubit NOT or :py:func:`PauliX` operator, i.e.,
    :math:`\\sqrt{\\texttt{NOT}}(\\sqrt{\\texttt{NOT}}) = X`.

    Parameters
    ----------
    d : int
        The number of qubits described by the state vector on which
        the produced operator will act.

    Returns
    -------
    Operator
        A rank `2d` tensor describing the operator.

    See Also
    --------
    Identity, PauliX, PauliY, PauliZ, Hadamard, Phase, CNOT, Toffoli
    Swap, SqrtSwap, ControlledU, U_f
    """

    return Operator(0.5 * np.array([[1 + 1j, 1 - 1j],
                                    [1 - 1j, 1 + 1j]])).tensor_power(d)


def CNOT():
    """
    Produce the two-qubit CNOT operator, which flips the second bit
    if the first bit is set.
    Maps \|00⟩ -> \|00⟩, \|01⟩ -> \|01⟩, \|10⟩ -> \|01⟩, \|11⟩ -> \|10⟩.

    Returns
    -------
    Operator
        A rank 4 tensor describing the operator.

    See Also
    --------
    Identity, PauliX, PauliY, PauliZ, Hadamard, Phase, Toffoli, SqrtNot
    Swap, SqrtSwap, ControlledU, U_f
    """

    return Operator((1.0 + 0.0j) *  np.array([[[[ 1.0, 0.0],
                                                [ 0.0, 1.0]],
                                               [[ 0.0, 0.0],
                                                [ 0.0, 0.0]]],
                                              [[[ 0.0, 0.0],
                                                [ 0.0, 0.0]],
                                               [[ 0.0, 1.0],
                                                [ 1.0, 0.0]]]]))


def Toffoli():
    """
    Produce the three-qubit Toffoli operator, which flips the third bit
    if the first two bits are set.
    Maps \|110⟩ -> \|111⟩, \|111⟩ -> \|110⟩, and otherwise acts as the
    identity.

    Returns
    -------
    Operator
        A rank 6 tensor describing the operator.

    See Also
    --------
    Identity, PauliX, PauliY, PauliZ, Hadamard, Phase, CNOT, SqrtNot
    Swap, SqrtSwap, ControlledU, U_f
    """

    d = 3
    shape = [2] * 2 * d
    t = np.zeros(shape, dtype=np.complex128)

    # Fill in the operator as the Identity operator.
    t[:] = Identity(d)[:]
    # In the case that the first two bits are set, it acts on the third
    # bit as the PauliX operator.
    t[:, 1, :, 1, ...] = (Identity(2) * PauliX())[:, 1, :, 1]

    return Operator(t)


def Swap():
    """
    Produce the two-qubit SWAP operator, which swaps two bits.
    Maps \|00⟩ -> \|00⟩, \|01⟩ -> \|10⟩, \|10⟩ -> \|01⟩, \|11⟩ -> \|11⟩.

    Returns
    -------
    Operator
        A rank 4 tensor describing the operator.

    See Also
    --------
    Identity, PauliX, PauliY, PauliZ, Hadamard, Phase, SqrtNot
    CNOT, Toffoli, SqrtSwap, ControlledU, U_f
    """

    return Operator((1.0 + 0.0j) *  np.array([[[[ 1.0, 0.0],
                                                [ 0.0, 0.0]],
                                               [[ 0.0, 0.0],
                                                [ 1.0, 0.0]]],
                                              [[[ 0.0, 1.0],
                                                [ 0.0, 0.0]],
                                               [[ 0.0, 0.0],
                                                [ 0.0, 1.0]]]]))


def SqrtSwap():
    """
    Produce the two-qubit operator that is the square root of the
    :py:func:`.Swap` operator, i.e.,
    :math:`\\sqrt{\\texttt{SWAP}}(\\sqrt{\\texttt{SWAP}}) = \\texttt{SWAP}`.

    Returns
    -------
    Operator
        A rank 4 tensor describing the operator.

    See Also
    --------
    Identity, PauliX, PauliY, PauliZ, Hadamard, Phase, SqrtNot
    CNOT, Toffoli, Swap, ControlledU, U_f
    """

    return Operator(np.array([[[[ 1.0,                 0.0],
                                [ 0.0,      0.5 * (1 + 1j)]],
                               [[ 0.0,                 0.0],
                                [ 0.5 * (1 - 1j),      0.0]]],
                              [[[ 0.0,       0.5 * (1 - 1j)],
                                [ 0.0,                 0.0]],
                               [[ 0.5 * (1 + 1j),      0.0],
                                [ 0.0,                 1.0]]]]))


def ControlledU(U):
    """
    Produce a Controlled-U operator, an operator for a `d` + 1 qubit
    system where the supplied U is an operator for a `d` qubit system.
    If the first bit is set, apply U to the state for the remaining
    bits.

    Parameters
    ----------
    U : Operator
        The operator to be conditionally applied.

    Returns
    -------
    Operator
        A tensor whose rank is the rank of U plus 2,
        describing the operator.

    See Also
    --------
    Identity, PauliX, PauliY, PauliZ, Hadamard, Phase, SqrtNot
    CNOT, Toffoli, Swap, SqrtSwap, U_f
    """

    d = U.rank // 2 + 1
    shape = [2] * 2 * d
    t = np.zeros(shape, dtype=np.complex128)

    # If the first bit is zero, fill in as the identity operator.
    t[:, 0, ...] = Identity(d)[:, 0, ...]
    # Else, fill in as Identity tensored with U (Identity for the first bit,
    # which remains unchanged.
    t[:, 1, ...] = (Identity() * U)[:, 1, ...]
    return Operator(t)


def U_f(f, d):
    """
    Produce a U_f operator, an operator for a `d` qubit
    system that flips the last bit based on the outcome of a supplied
    boolean function :math:`f: [0, 1]^{d-1} \\to [0, 1]` applied to the
    first `d` - 1 bits.

    Parameters
    ----------
    f : function
        The boolean function used to conditionally flip the last bit.

    Returns
    -------
    Operator
        A rank `2d` tensor describing the operator.

    See Also
    --------
    Identity, PauliX, PauliY, PauliZ, Hadamard, Phase, SqrtNot
    CNOT, Toffoli, Swap, SqrtSwap, ControlledU
    """
    if d < 2:
        raise ValueError('U_f operator requires rank >= 2.')

    operator_shape = [2] * 2 * d
    t = np.zeros(operator_shape, dtype=np.complex128)

    for bits in product([0, 1], repeat=d):
        input_bits = bits[:-1]
        result = f(*input_bits)

        if result not in [0, 1]:
            raise RuntimeError('Function f for U_f operator should be Boolean,' \
                               'i.e., return 0 or 1.')

        result_bits = list(bits)
        if result:
            result_bits[-1] = 1 - result_bits[-1]
        all_bits = tuple([item for sublist in zip(result_bits, bits) for item in sublist])

        t[all_bits] = 1.0 + 0.0j

    return Operator(t)
