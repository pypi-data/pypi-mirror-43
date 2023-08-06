Quantum Spin
============

This is a little package that will help with learning how quantum spin and entanglement work.
It is meant to complement some of the "theoretical minimum" lectures and other web resources:

[
`Quantum state <https://en.wikipedia.org/wiki/Quantum_state>`_; 
`Pauli matrices <https://en.wikipedia.org/wiki/Pauli_matrices>`_;
`Singlet state <https://en.wikipedia.org/wiki/Singlet_state>`_;
`Triplet state <https://en.wikipedia.org/wiki/Triplet_state>`_;
`Density matrix <https://en.wikipedia.org/wiki/Density_matrix>`_;
`Quantum entanglement <https://en.wikipedia.org/wiki/Quantum_entanglement>`_;
`Entropy <https://en.wikipedia.org/wiki/Von_Neumann_entropy>`_;
`Quantum logic gate <https://en.wikipedia.org/wiki/Quantum_logic_gate>`_
]

- Book: **Quantum Mechanics - The Theoretical Minimum**, Leanoard Susskind and Art Friedman, Basic Books, 2014. (mostly chapters 6&7)
- http://theoreticalminimum.com/courses/quantum-mechanics/2012/winter/lecture-6 and lecture-7

`Link to documentation on readthedocs <http://qspin.readthedocs.io>`_

**Install**
------------

.. code:: bash

    pip install --upgrade qspin
    
**Out-of-the box tests:**
--------------------------
.. code:: python

    $ python
    >>> import qspin
    >>> qspin.all_tests()

Examples of code use
--------------------

**Spin states**
~~~~~~~~~~~~~~~~~~~~~~~~~~

up, down and linear combinations to form mixed states

.. code:: python

    >>> from qspin import bra,ket,u,d,s0,sx,sy,sz
    >>> u
    |u> 
    >>> d
    |d> 
    >>> u + d
    |u>  + |d>
    >>> i = 1j
    >>> u + i*d
    |u>  + i |d> 

**Operators**
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    >>> sx # Pauli spin matrix
    [[0 1]
     [1 0]]
    >>> sy
    [[ 0.+0.j -0.-1.j]
     [ 0.+1.j  0.+0.j]]
    >>> sz
    [[ 1  0]
     [ 0 -1]]
    >>> sz*u
    |u>
    >>> sz*d
    - |d>

**Expected value of an observable**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

sz is the observable for z-component of spin, For the "up" state, the only
outcome us +1, so the expected value is +1.

.. code:: python

    >> u.H*sz*u
    1.0
    >> sz.average(u) # another way to compute the average of an observable
    1.0

(`q.H` is Hermetian conjugate; it converts a ket to a bra, as in :math:`\Braket{u|s_z|u}`).
The operator (sz in this case) is known in quantum mechanics as an observable,
meaning it measures something. Here it is the z-component of spin.
The eigenvalues of the observable are the possible outcomes the observation.
Underlying each state is a wave function. We store the wave function internally
as vector, with each component being the wave function value for the basis eigenstate.
The operators (observables) are stored as matrices, also defined on the same basis.
The assumed basis throughout qspin is :math:`\Ket{u}` and :math:`\Ket{d}` for single particles.

.. code:: python

    >>> u
    |u> 
    >>> u.phi
    matrix([[ 1.],
            [ 0.]])

**Eigenvalues**
~~~~~~~~~~~~~~~~~~~~~~~~~~

We can evaluate the eigenvalues and eigenvectors of observables. ".matrix" pulls out the matrix
representation of the operator.

.. code:: python

    >>> import numpy as np
    >>> sz
    [[ 1  0]
     [ 0 -1]]
    >>> ev, evec = np.linalg.eig(sz.matrix)
    >>> ev
    array([ 1., -1.])
    >>> evec
    matrix([[ 1.,  0.],
            [ 0.,  1.]])
    >>> sx # spin x
    [[0 1]
     [1 0]]
    >>> ev, evec = np.linalg.eig(sx.matrix)
    >>> ev
    array([ 1., -1.])
    >>> evec
    matrix([[ 0.70710678, -0.70710678],
            [ 0.70710678,  0.70710678]])

There is a handy 'eig' method that produces a list of eigenvalues and a
list of eigenvectors, with the eigenvectors being states:

.. code:: python

    >>> ev, evec = sx.eig()
    >>> ev
    array([1.,=1.])
    >>> evec
    [0.707107 |u> + 0.707107 |d> , -0.707107 |u> + 0.707107 |d> ]
    >>> sz.eig()
    (array([ 1., -1.]), [|u> , |d> ])

Note that the spin-x observerable has the same eigenvalues as spin-z, +1 and -1. But the eigenvectors
are different, in our basis, since we are using the {:math:`\Ket{u}`, :math:`\Ket{d}`} basis. They are
:math:`(\Ket{u} + \Ket{d})/\sqrt{2}`, which measures as sx = +1, and
:math:`(\Ket{u} - \Ket{d})/\sqrt{2}`, which measures as sx = -1.

**Conditional Probabilities**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Conditional probabilities are calculated using inner products of states with the
eigenvectors of the measurment, squared. So the probability
of measuring sx = +1 given the particle is prepared in state :math:`\Ket{u}` is:

.. code:: python

    >>> l = (u+d).N # "left" state. The .N normalizes the state
    >>> (bra(l)*ket(u))**2   # expected value of up given left
    0.5
    >>> np.abs( l.H * u )**2 # another way to do this. The .H means Hermetian conjugate; converts ket to bra
    0.5
    >>> l.prob(sx,l)
    1.0
    >>> l.prob(sx,u)
    0.5
    

**Measurement**
~~~~~~~~~~~~~~~~~~~~~~~~~~

The quantum measurement of an observable involves 'collapsing' the state
to one of the eigen states of the obserable.

.. code:: python

    >>> l = (u+d).N
    >>> sz.measure(l)
    (1.0, |u>)

The result is random, either up or down
(with 50-50 probability in this case where the particle starts out in state 'spin left').
The measure function returns the value of the measurment, 1.0 in this case,
and the collapsed state, :math:`\Ket{u}`.

**String Representation of State**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We can use strings to refer to basis states.

.. code:: python

    >>> u = ket('|u>') # or ket('u')  (the vert line and bracket are optional)
    >>> d = ket('|d>') # or ket('d')
    >>> u
    |u>
    >>> d
    |d>

The string representation of basis functions defaults to 'u' and 'd'. As
an alternative, the representation can be set to
'0' and '1' or to up and down arrows (the later require your
terminal to have the ability to display unicode characters).

.. code:: python

    >>> qspin.set_base_repr('01')
    >>> u = ket('0')
    >>> d = ket('1')
    >>> (u + d).N
    0.707107 |0> + 0.707107 |1>

With :code:`qspin.set_base_repr('arrow')`, :code:`u=ket([1,0])` renders as :math:`\Ket{\uparrow}`
This provides cute printout, but is not too useful for string entry, since the up and
down arrows are unicode.

**Wave Function Definition**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

States can also be defined using the wave function, given
in the form of a matrix column vector. And it is good practice
to normalize states.

.. code:: python

    >>> w = ket( np.matrix([1.,1.]).T).N
    >>> w
    0.707106781187 |u>  + 0.707106781187 |d> 
    

Form a projection operator from outer products of basis states.

.. code:: python

    >> rho = ket('|u>') * bra('<u|') + ket('|d>') * bra('<d|')
    >> # can also do this:
    >> u = ket('|u>'); d = ket('|d>');
    >> rho = ket(u) * bra(u) + ket(d) * bra(d)
    >>> rho
    [[ 1.  0.]
     [ 0.  1.]]
    >>> u
    1.0 |u> 
    >>> rho*u
    1.0 |u> 
    >>> rho*d
    1.0 |d> 

Note that bra(ket(...)) and ket(bra(...)) convert, and takes care of the complex-conjugating.

.. code:: python

    >> u.kind
    'ket'
    >> bra(u).kind
    'bra'

**Density Matrix and Entropy**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a density matrix for an ensemble of single particles.

.. code:: python

    >> from qspin import entropy
    >> P = [0.5, 0.5]
    >> rho = P[0] * bra('|u>').density() + P[1] * bra('|d>').density() # make sure the probabilities add to one
    >> entropy(rho) # it's not zero because there is a mixture of states
    0.69314718055994529
    >> rho = ( bra('|u>') + bra('|d>') ).N.density()
    >> entropy(rho) # this is zero because all electrons are prepared in the "u+d" state
    0
    
Make sure you normalize any states you define, using the post-operation .N.

The von Neumann **entropy** is
:math:`S = -\sum_i(p_i log(p_i))` where :math:`p_i` are the density matrix eigenvalues.
The entropy is essentially the randomness in a measurement of the quantum state. It
can be applied to any density matrix for either pure or mixed states. (A
pure state has zero entropy.)

**Multi-particle States**
~~~~~~~~~~~~~~~~~~~~~~~~~~

Multi-particle states are in the space formed from the Kronecker product of Hilbert spaces
of the individual particles. Since multi-particle quantum states can be mixed states, there
are far more possible state vectors (:math:`2^n` dimensional vector space) than for classical
systems (which are in only :math:`n` dimensional space)

We build up multi-particle states with Kronecker products '**' (meaning :math:`\otimes`), or with strings

.. code:: python

    >>> uu = u**u
    >>> dd = ket('|dd>') # or ket('dd')
    >>> s = (d**u**u + u**d**u + d**d**u).N
    >>> s
    0.57735 |udu> + 0.57735 |duu> + 0.57735 |ddu> 
    
Multi-particle operators are similarly built up with Kronecker products

.. code:: python

    >>> s2x = sx**sx
    >>> s2x
    [[0 0 0 1]
     [0 0 1 0]
     [0 1 0 0]
     [1 0 0 0]

**Partial Trace**
~~~~~~~~~~~~~~~~~~~~~~~~~~

The density matrix for a multi-particle state is :math:`2^n \times 2^n`. A partial
trace is a way to form the density matrix for a subset of the particles. 'Tracing out'
:math:`m` of the particles results in a :math:`2^{n-m} \times 2^{n-m}` density matrix.
Partial traces are important in many aspects of analyzing the multi-particle state,
including evaluating the entanglement.

.. code:: python

    >>> sing = (u**d - d**u).N
    >>> rho = sing.density()
    >>> rho
    matrix([[ 0. ,  0. ,  0. ,  0. ],
            [ 0. ,  0.5, -0.5,  0. ],
            [ 0. , -0.5,  0.5,  0. ],
            [ 0. ,  0. ,  0. ,  0. ]])
    >>> rhoA = ptrace(rho,[1]) # trace over particle 1 ('Bob') to get particle 0 ('Alice') density
    >>> rhoA
    matrix([[0.5, 0. ],
            [0. , 0.5]])

**Entangled States**
~~~~~~~~~~~~~~~~~~~~~~~~~~

Once you have created a (possibly) entangled state of two particles, you can test it for entanglement:

.. code:: python

    >>> sing = (u**d - d**u).N
    >>> sing.entangled()
    True
    >>> (u**u).entangled()
    False

The test for entanglement is to check the entropy of one of the particles after
the other particle has been 'traced out.'

Quantum Computing
~~~~~~~~~~~~~~~~~~~~~~~~~~


Several quantum logic gates are now defined in qspin including:
Hadamard, NOT, SWAP, controlled gates, square root gates, and phase shift gates.

.. code:: python

    >>> from qspin import u,d,gate
    >>> SWAP = gate('SWAP')
    >>> SWAP*(u**d)
    |du>
    >>> H = gate('Hadamard')
    >>> H*u
    0.707 |u> + 0.707 |d> 
    >>> H*d
    0.707 |u> - 0.707 |d>
    
shows that SWAP interchanges the q-bits, and Hadamard makes the Bell states
from spin up and spin down.
