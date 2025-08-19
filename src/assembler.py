from src.machine import get_register
from src.register import set_contents, get_contents


def assemble(controller_text, machine):
    insts, labels = extract_labels(controller_text)
    update_insts(insts, labels, machine)
    return insts


def extract_labels(text):
    insts = []
    labels = {}
    for label_or_inst in text:
        if isinstance(label_or_inst, str):
            labels[label_or_inst] = len(insts)
        else:
            insts.append(label_or_inst)
    return insts, labels


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


def make_execution_procedure(inst, labels, machine, pc, flag, stack, ops):
    if inst[0] == "assign":
        return make_assign(inst, machine, labels, ops, pc)
    else:
        raise Exception(f"unknown instruction type -- ASSEMBLE {inst}")


def make_assign(inst, machine, labels, operations, pc):
    target = get_register(machine, assign_reg_name(inst))
    value_exp = assign_value_exp(inst)
    if value_exp[0][0] == "op":
        value_proc = make_operation_exp(value_exp, machine, labels, operations)
    else:
        value_proc = make_primitive_exp(value_exp[0], machine, labels)

    def proc():
        set_contents(target, value_proc())
        advance_pc(pc)

    return proc


def assign_reg_name(assign_instruction):
    return assign_instruction[1][0]


def assign_value_exp(assign_instruction):
    return assign_instruction[1][1:]


def make_primitive_exp(exp, machine, labels):
    keyword, value = exp
    if keyword == "const":  # ["const", 0]
        return lambda: value
    elif keyword == "label":  # ["label", "loop"]
        idx = labels[value]
        return lambda: idx
    elif keyword == "reg":  # ["reg", "n"]
        r = get_register(machine, value)
        return lambda: get_contents(r)
    else:
        raise Exception(f"unknown expression type -- ASSEMBLE {exp}")


def make_operation_exp(exp, machine, labels, operations):
    _, op_name = exp[0]
    op = operations[op_name]
    operands = exp[1:]
    aprocs = [make_primitive_exp(operand, machine, labels) for operand in operands]
    return lambda: op(*[proc() for proc in aprocs])


def advance_pc(pc):
    set_contents(pc, get_contents(pc) + 1)
