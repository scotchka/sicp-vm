import pytest
from src.machine import make_new_machine, start


def test_start():
    machine = make_new_machine()
    machine("install-instruction-sequence")([])

    assert start(machine) == "done"


def test_allocate_register():
    machine = make_new_machine()
    machine("allocate-register")("abc")
    register = machine("get-register")("abc")
    assert register.get_contents() is None


def test_allocate_register_exception():
    machine = make_new_machine()
    with pytest.raises(ValueError, match="Multiply defined register: pc"):
        machine("allocate-register")("pc")


def test_install_operations():
    machine = make_new_machine()
    machine("install-operations")([("op",)])
    assert machine("operations")[-1] == ("op",)


def test_machine_exception():
    machine = make_new_machine()
    with pytest.raises(ValueError, match="Unknown request nope"):
        machine("nope")
