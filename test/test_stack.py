import pytest
from src.stack import make_stack, push, pop


def test_stack():
    stack = make_stack()

    push(stack, 1)
    push(stack, 2)
    push(stack, 3)

    assert pop(stack) == 3
    assert pop(stack) == 2
    assert pop(stack) == 1


def test_initialize():
    stack = make_stack()

    push(stack, 1)
    push(stack, 2)
    push(stack, 3)

    stack("initialize")

    with pytest.raises(RuntimeError):
        stack("pop")


def test_unknown_message():
    stack = make_stack()

    with pytest.raises(ValueError):
        stack("nope")
