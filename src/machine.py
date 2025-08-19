from src.register import Register
from src.stack import Stack


def make_machine(register_names, ops, controller_text):
    from src.assembler import assemble

    machine = make_new_machine()
    for register_name in register_names:
        machine("allocate-register")(register_name)
    machine("install-operations")(ops)
    machine("install-instruction-sequence")(assemble(controller_text, machine))
    return machine


def make_new_machine():
    pc = Register()
    flag = Register()
    stack = Stack()
    instructions = []
    ops = [("initialize-stack", lambda: stack.__init__())]
    registers = {"pc": pc, "flag": flag}

    def allocate_register(name):
        if name in registers:
            raise ValueError(f"Multiply defined register: {name}")
        registers[name] = Register()
        return "register allocated"

    def lookup_register(name):
        return registers[name]

    def execute():
        insts = pc.get_contents()
        if insts == []:
            return "done"
        proc = instruction_execution_proc(insts[0])
        proc()
        return execute()

    def dispatch(message):
        if message == "start":
            pc.set_contents(instructions)
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


def get_register_contents(machine, register_name):
    return get_register(machine, register_name).get_contents()


def set_register_contents(machine, register_name, value):
    get_register(machine, register_name).set_contents(value)
    return "done"


def get_register(machine, register_name):
    return machine("get-register")(register_name)


def instruction_execution_proc(inst):
    text, proc = inst
    return proc
