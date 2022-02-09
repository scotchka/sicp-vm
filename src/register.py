def make_register(name):
    contents = None

    def dispatch(message):
        if message == "get":
            return contents
        elif message == "set":

            def set_value(value):
                nonlocal contents
                contents = value

            return set_value
        else:
            raise ValueError(f"Unknown request {message}")

    return dispatch


def get_contents(register):
    return register("get")


def set_contents(register, value):
    return register("set")(value)
