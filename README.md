# A Register-Machine Simulator

This is a Python implementation of section 5.2 of 
[Structure and Interpretation of Computer Programs](https://web.mit.edu/6.001/6.037/sicp.pdf)

The most significant deviation from the original Scheme is the use of arrays (Python lists) instead
of linked lists. This has as a consequence, for example, that the program counter is an index in the
instructions list rather than a reference to a link.
