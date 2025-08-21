from src.stack import Stack
from src.assembler import assemble


class Machine:
    def __init__(self, register_names, ops, controller_text):
        self.stack = Stack()
        self.ops = ops
        self.registers = {"pc": 0, "flag": 0}

        for register_name in register_names:
            if register_name in self.registers:
                raise ValueError(
                    f"Multiply defined register: {register_name}"
                )  # pragma: no cover
            self.registers[register_name] = 0

        self.instructions = assemble(controller_text, self)

    def execute(self):
        idx = self.registers["pc"]
        if idx == len(self.instructions):
            return "done"
        _, proc = self.instructions[idx]
        proc()
        return self.execute()

    def start(self):
        self.registers["pc"] = 0
        return self.execute()
