def make_stack():
    s = []

    def push(x):
        nonlocal s
        s = [x] + s

    def pop():
        nonlocal s
        if s == []:
            raise RuntimeError("Empty stack")
        top = s[0]
        s = s[1:]
        return top

    def initialize():
        nonlocal s
        s = []
        return "done"

    def dispatch(message):
        if message == "push":
            return push
        elif message == "pop":
            return pop()
        elif message == "initialize":
            return initialize()
        else:
            raise ValueError(f"Unknown request {message}")

    return dispatch


def pop(stack):
    return stack("pop")


def push(stack, value):
    return stack("push")(value)
