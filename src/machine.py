from src.register import Register
from src.stack import Stack


def make_machine(register_names, ops, controller_text):
    from src.assembler import assemble

    machine = Machine()
    for register_name in register_names:
        machine("allocate-register")(register_name)
    machine("install-operations")(ops)
    machine("install-instruction-sequence")(assemble(controller_text, machine))
    return machine


class Machine:
    def __init__(self):
        self.pc = Register()
        self.flag = Register()
        self.stack = Stack()
        self.instructions = []
        self.ops = {"initialize-stack": lambda: self.stack.__init__()}
        self.registers = {"pc": self.pc, "flag": self.flag}

    def allocate_register(self, name):
        if name in self.registers:
            raise ValueError(f"Multiply defined register: {name}")
        self.registers[name] = Register()
        return "register allocated"

    def lookup_register(self, name):
        return self.registers[name]

    def execute(self):
        insts = self.pc.get_contents()
        if insts == []:
            return "done"
        proc = instruction_execution_proc(insts[0])
        proc()
        return self.execute()

    def start(self):
        self.pc.set_contents(self.instructions)
        return self.execute()

    def install_instructions(self, instructions):
        self.instructions = instructions

    def install_operations(self, ops):
        self.ops.update(ops)


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
