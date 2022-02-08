import pytest
from src.register import make_register, set_contents, get_contents


def test_register():
    register = make_register("test")
    set_contents(register, "hello")
    assert get_contents(register) == "hello"


def test_register_exception():
    register = make_register("test")
    with pytest.raises(ValueError, match="Unknown request nope"):
        register("nope")
