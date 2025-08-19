import pytest
from src.machine import Machine


def test_start():
    machine = Machine()
    machine.install_instructions([])

    assert machine.start() == "done"


def test_allocate_register():
    machine = Machine()
    machine.allocate_register("abc")
    register = machine.registers["abc"]
    assert register.get_contents() is None


def test_allocate_register_exception():
    machine = Machine()
    with pytest.raises(ValueError, match="Multiply defined register: pc"):
        machine.allocate_register("pc")


def test_install_operations():
    machine = Machine()
    machine.install_operations({"a": 1})
    assert machine.ops["a"] == 1
