from src.machine import Machine


def test_assign_const():
    machine = Machine(["a"], {}, ["start", ["assign", "a", ["const", 5]], "done"])

    machine.start()

    assert machine.registers == {"a": 5, "pc": 1, "flag": 0}


def test_assign_label():
    machine = Machine(["a"], {}, ["start", ["assign", "a", ["label", "start"]], "done"])

    machine.start()

    assert machine.registers == {"a": 0, "pc": 1, "flag": 0}


def test_assign_register():
    machine = Machine(
        ["a", "b"],
        {},
        [
            "start",
            ["assign", "b", ["const", 10]],
            ["assign", "a", ["reg", "b"]],
            "done",
        ],
    )

    machine.start()

    assert machine.registers == {"a": 10, "b": 10, "pc": 2, "flag": 0}


def test_assign_op():
    machine = Machine(
        ["a"],
        {"+": int.__add__},
        ["start", ["assign", "a", ["op", "+"], ["const", 3], ["const", 4]], "done"],
    )

    machine.start()

    assert machine.registers == {"a": 7, "pc": 1, "flag": 0}


def test_make_test():
    machine = Machine(
        [],
        {"=": lambda a, b: int(a == b)},
        ["start", ["test", ["op", "="], ["const", 4], ["const", 4]], "done"],
    )

    machine.start()

    assert machine.registers == {"pc": 1, "flag": 1}


def test_make_branch_true():
    machine = Machine(
        [],
        {},
        [
            "start",
            ["assign", "flag", ["const", 1]],
            ["branch", ["label", "done"]],
            ["assign", "flag", ["const", 0]],  # this line should be skipped
            "done",
        ],
    )

    machine.start()

    assert machine.registers == {"pc": 3, "flag": 1}


def test_make_branch_false():
    machine = Machine(
        [],
        {},
        [
            "start",
            ["assign", "flag", ["const", 0]],
            ["branch", ["label", "done"]],
            ["assign", "flag", ["const", 1]],  # this line should be executed
            "done",
        ],
    )

    machine.start()

    assert machine.registers == {"pc": 3, "flag": 1}


def test_goto_label():
    machine = Machine(
        [],
        {},
        [
            "start",
            ["goto", ["label", "done"]],
            ["assign", "flag", ["const", 99]],  # this line should be skipped
            "done",
        ],
    )

    machine.start()

    assert machine.registers == {"pc": 2, "flag": 0}


def test_goto_register():
    machine = Machine(
        [],
        {},
        [
            "start",
            ["assign", "flag", ["label", "done"]],
            ["goto", ["reg", "flag"]],
            ["assign", "flag", ["const", 99]],  # this line should be skipped
            "done",
        ],
    )

    machine.start()

    assert machine.registers == {"pc": 3, "flag": 3}
