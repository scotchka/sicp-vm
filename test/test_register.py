from src.register import Register


def test_register():
    register = Register()
    register.set_contents("hello")
    assert register.get_contents() == "hello"
