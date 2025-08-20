from src.stack import Stack
from src.assembler import assemble


class Machine:
    def __init__(self, register_names, ops, controller_text):
        self.stack = Stack()
        self.instructions = []
        self.ops = {"initialize-stack": lambda: self.stack.__init__()}
        self.registers = {"pc": 0, "flag": None}

        for register_name in register_names:
            self.allocate_register(register_name)
        self.install_operations(ops)
        self.install_instructions(assemble(controller_text, self))

    def allocate_register(self, name):
        if name in self.registers:
            raise ValueError(f"Multiply defined register: {name}")
        self.registers[name] = None
        return "register allocated"

    def execute(self):
        idx = self.registers["pc"]
        if idx == len(self.instructions):
            return "done"
        text, proc = self.instructions[idx]
        proc()
        return self.execute()

    def start(self):
        self.registers["pc"] = 0
        return self.execute()

    def install_instructions(self, instructions):
        self.instructions = instructions

    def install_operations(self, ops):
        self.ops.update(ops)
