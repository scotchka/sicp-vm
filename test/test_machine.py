from src.machine import make_new_machine, start


def test_start():
    machine = make_new_machine()
    print(machine)
    machine("install-instruction-sequence")([])

    assert start(machine) == "done"
