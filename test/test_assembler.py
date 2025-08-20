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


def test_gcd_machine():
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


def test_save():
    machine = Machine(
        [],
        {},
        [
            "start",
            ["assign", "flag", ["const", 1]],
            ["save", "flag"],
            ["assign", "flag", ["const", 2]],
            ["save", "flag"],
            "done",
        ],
    )

    machine.start()

    assert machine.registers == {"pc": 4, "flag": 2}
    assert machine.stack._stack == [1, 2]


def test_restore():
    machine = Machine(
        [],
        {},
        [
            "start",
            ["assign", "flag", ["const", 1]],
            ["save", "flag"],
            ["assign", "flag", ["const", 2]],
            ["save", "flag"],
            ["assign", "flag", ["const", 3]],
            ["restore", "flag"],
            "done",
        ],
    )

    machine.start()

    assert machine.registers == {"pc": 6, "flag": 2}
    assert machine.stack._stack == [1]
