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
            insts.append([label_or_inst, None])
    return insts, labels


def update_insts(insts, labels, machine):

    stack = machine.stack
    ops = machine.ops

    for inst in insts:
        inst[1] = make_execution_procedure(inst[0], labels, machine, stack, ops)


def make_execution_procedure(inst, labels, machine, stack, ops):
    if inst[0] == "assign":
        return make_assign(inst, machine, labels, ops)

    raise Exception(f"unknown instruction type -- ASSEMBLE {inst}")  # pragma: no cover


def make_assign(inst, machine, labels, operations):
    # e.g. ["assign", "t", ...]
    reg_name = inst[1]
    value_exp = inst[2:]
    if value_exp[0][0] == "op":
        value_proc = make_operation_exp(value_exp, machine, labels, operations)
    else:
        value_proc = make_primitive_exp(value_exp[0], machine, labels)

    def proc():
        machine.registers[reg_name] = value_proc()
        machine.registers["pc"] += 1

    return proc


def make_primitive_exp(exp, machine, labels):
    keyword, value = exp
    if keyword == "const":  # ["const", 0]
        return lambda: value
    elif keyword == "label":  # ["label", "loop"]
        idx = labels[value]
        return lambda: idx
    elif keyword == "reg":  # ["reg", "n"]
        return lambda: machine.registers[value]

    raise Exception(f"unknown expression type -- ASSEMBLE {exp}")  # pragma: no cover


def make_operation_exp(exp, machine, labels, operations):
    _, op_name = exp[0]
    op = operations[op_name]
    operands = exp[1:]
    aprocs = [make_primitive_exp(operand, machine, labels) for operand in operands]
    return lambda: op(*[proc() for proc in aprocs])
