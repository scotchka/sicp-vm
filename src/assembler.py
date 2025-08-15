from src.machine import get_register


def assemble(controller_text, machine):
    def receive(insts, labels):
        update_insts(insts, labels, machine)
        return insts

    return extract_labels(controller_text, receive)


def extract_labels(text, receive):
    if not text:
        return receive([], {})

    def new_receive(insts, labels):
        next_inst = text[0]
        if isinstance(next_inst, str):
            return receive(insts, {next_inst: insts} | labels)
        else:
            return receive([make_instruction(next_inst)] + insts, labels)

    return extract_labels(text[1:], new_receive)


def update_insts(insts, labels, machine):
    pc = get_register(machine, "pc")
    flag = get_register(machine, "flag")
    stack = machine("stack")
    ops = machine("operations")

    def apply(inst):
        set_instruction_execution_proc(
            inst,
            make_execution_procedure(
                instruction_text(inst), labels, machine, pc, flag, stack, ops
            ),
        )

    for inst in insts:
        apply(inst)


def make_instruction(text):
    return [text, None]


def instruction_text(inst):
    text, proc = inst
    return text


def set_instruction_execution_proc(inst, proc):
    inst[1] = proc
