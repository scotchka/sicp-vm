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


def test_gcd_machine(mocker):
    print_mock = mocker.patch("builtins.print")
    mocker.patch("builtins.input", side_effect=["18", "12"])
    machine = Machine(
        ["a", "b", "t"],
        {
            "rem": lambda a, b: a % b,
            "=": lambda a, b: int(a == b),
            "print": print,
            "read": lambda: int(input("enter an integer: ")),
        },
        [
            "gcd-loop",
            ["assign", "a", ["op", "read"]],
            ["assign", "b", ["op", "read"]],
            "test-b",
            ["test", ["op", "="], ["reg", "b"], ["const", 0]],
            ["branch", ["label", "gcd-done"]],
            ["assign", "t", ["op", "rem"], ["reg", "a"], ["reg", "b"]],
            ["assign", "a", ["reg", "b"]],
            ["assign", "b", ["reg", "t"]],
            ["goto", ["label", "test-b"]],
            "gcd-done",
            ["perform", ["op", "print"], ["reg", "a"]],
        ],
    )

    machine.start()

    print_mock.assert_called_once_with(6)


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


def test_factorial():
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


def test_fibonacci():
    machine = Machine(
        ["n", "val", "continue"],
        {
            "<": int.__lt__,
            "-": int.__sub__,
            "+": int.__add__,
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
        ],
    )
    for n, expected in zip(range(1, 9), [1, 1, 2, 3, 5, 8, 13, 21]):
        machine.registers["n"] = n
        machine.start()
        assert machine.registers["val"] == expected
