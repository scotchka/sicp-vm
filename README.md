# A Register-Machine Simulator

This is a Python implementation of section 5.2 of 
[Structure and Interpretation of Computer Programs](https://web.mit.edu/6.001/6.037/sicp.pdf)

The most significant deviation from the original Scheme is the use of arrays (Python lists) instead
of linked lists. This has as a consequence, for example, that the program counter is an index in the
instructions list rather than a reference to a link.

## Example: greatest common divisor

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

## Example: factorial

```python
machine = Machine(
    ["continue", "n", "val"],
    {"=": lambda a, b: int(a == b), "-": int.__sub__, "*": int.__mul__},
    [
        "controller",
        ["assign", "continue", ["label", "fact-done"]],
        "fact-loop",
        ["test", ["op", "="], ["reg", "n"], ["const", 1]],
        ["branch", ["label", "base-case"]],
        ["save", "continue"],
        ["save", "n"],
        ["assign", "n", ["op", "-"], ["reg", "n"], ["const", 1]],
        ["assign", "continue", ["label", "after-fact"]],
        ["goto", ["label", "fact-loop"]],
        "after-fact",
        ["restore", "n"],
        ["restore", "continue"],
        ["assign", "val", ["op", "*"], ["reg", "n"], ["reg", "val"]],
        ["goto", ["reg", "continue"]],
        "base-case",
        ["assign", "val", ["const", 1]],
        ["goto", ["reg", "continue"]],
        "fact-done",
    ],
)

machine.registers["n"] = 6

machine.start()

assert machine.registers["val"] == 6 * 5 * 4 * 3 * 2 * 1
```

## Example: Fibonacci sequence

```python
machine = Machine(
    ["n", "val", "continue"],
    {
        "<": int.__lt__,
        "-": int.__sub__,
        "+": int.__add__,
        "print": print
    },
    [
        "controller",
        ["assign", "continue", ["label", "fib-done"]],
        "fib-loop",
        ["test", ["op", "<"], ["reg", "n"], ["const", 2]],
        ["branch", ["label", "immediate-answer"]],
        ["save", "continue"],
        ["assign", "continue", ["label", "afterfib-n-1"]],
        ["save", "n"],
        ["assign", "n", ["op", "-"], ["reg", "n"], ["const", 1]],
        ["goto", ["label", "fib-loop"]],
        "afterfib-n-1",
        ["restore", "n"],
        ["restore", "continue"],
        ["assign", "n", ["op", "-"], ["reg", "n"], ["const", 2]],
        ["save", "continue"],
        ["assign", "continue", ["label", "afterfib-n-2"]],
        ["save", "val"],
        ["goto", ["label", "fib-loop"]],
        "afterfib-n-2",
        ["assign", "n", ["reg", "val"]],
        ["restore", "val"],
        ["restore", "continue"],
        ["assign", "val", ["op", "+"], ["reg", "val"], ["reg", "n"]],
        ["goto", ["reg", "continue"]],
        "immediate-answer",
        ["assign", "val", ["reg", "n"]],
        ["goto", ["reg", "continue"]],
        "fib-done",
        ["perform", ["op", "print"], ["reg", "val"]]
    ],
)

for n in range(1, 11):
    machine.registers["n"] = n
    machine.start()
```

This should print out:
```
1
1
2
3
5
8
13
21
34
55
```
