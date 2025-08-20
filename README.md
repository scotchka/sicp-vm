# A Register-Machine Simulator

This is a Python implementation of section 5.2 of 
[Structure and Interpretation of Computer Programs](https://web.mit.edu/6.001/6.037/sicp.pdf)

The most significant deviation from the original Scheme is the use of arrays (Python lists) instead
of linked lists. This has as a consequence, for example, that the program counter is an index in the
instructions list rather than a reference to a link.

## Example: greatest common divisor (p. 514)

```python
from src.machine import Machine


machine = Machine(
    ["a", "b", "t"],
    {"rem": lambda a, b: a % b, "=": lambda a, b: int(a == b)},
    [
        "test-b",
        ["test", ["op", "="], ["reg", "b"], ["const", 0]],
        ["branch", ["label", "gcd-done"]],
        ["assign", "t", ["op", "rem"], ["reg", "a"], ["reg", "b"]],
        ["assign", "a", ["reg", "b"]],
        ["assign", "b", ["reg", "t"]],
        ["goto", ["label", "test-b"]],
        "gcd-done",
    ],
)

machine.registers["a"] = 12
machine.registers["b"] = 18

machine.start()

assert machine.registers["a"] == 6
```
