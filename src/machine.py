from src.register import make_register, get_contents, set_contents
from src.stack import make_stack


def make_new_machine():
    pc = make_register("pc")
    flag = make_register("flag")
    stack = make_stack()
    instructions = []
    ops = [("initialize-stack", lambda: stack("initialize"))]
    registers = {"pc": pc, "flag": flag}

    def allocate_register(name):
        if name in registers:
            raise ValueError(f"Multiply defined register: {name}")
        registers[name] = make_register(name)
        return "register allocated"

    def lookup_register(name):
        return registers[name]

    def execute():
        insts = get_contents(pc)
        if insts == []:
            return "done"
        instruction_execution_proc(insts[0])
        return execute()

    def dispatch(message):
        if message == "start":
            set_contents(pc, instructions)
            return execute()
        elif message == "install-instruction-sequence":

            def install_instructions(seq):
                nonlocal instructions
                instructions = seq

            return install_instructions

        elif message == "allocate-register":
            return allocate_register
        elif message == "get-register":
            return lookup_register
        elif message == "install-operations":

            def install_operations(new_ops):
                nonlocal ops
                ops = ops + new_ops

            return install_operations
        elif message == "stack":
            return stack
        elif message == "operations":
            return ops
        else:
            raise ValueError(f"Unknown request {message}")

    return dispatch


def start(machine):
    return machine("start")
