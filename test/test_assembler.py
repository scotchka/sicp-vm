from src import machine
from src.machine import Machine


def test_assign_const():
    machine = Machine(["a"], {}, ["start", ["assign", "a", ["const", 5]], "done"])

    machine.start()

    assert machine.registers == {"a": 5, "pc": 1, "flag": None}


def test_assign_label():
    machine = Machine(["a"], {}, ["start", ["assign", "a", ["label", "start"]], "done"])

    machine.start()

    assert machine.registers == {"a": 0, "pc": 1, "flag": None}


def test_assign_register():
    machine = Machine(["a", "b"], {}, ["start", ["assign", "a", ["reg", "b"]], "done"])

    machine.registers["b"] = 10
    machine.start()

    assert machine.registers == {"a": 10, "b": 10, "pc": 1, "flag": None}
