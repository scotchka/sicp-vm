def assemble(controller_text, registers, ops, stack):
    insts, labels = extract_labels(controller_text)
    update_insts(insts, labels, registers, ops, stack)
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


def update_insts(insts, labels, registers, ops, stack):

    for inst in insts:
        inst[1] = make_execution_procedure(inst[0], labels, registers, ops, stack)


def make_execution_procedure(inst, labels, registers, ops, stack):
    if inst[0] == "assign":
        return make_assign(inst, registers, ops, labels)
    if inst[0] == "test":
        return make_test(inst, registers, ops, labels)
    if inst[0] == "branch":
        return make_branch(inst, registers, labels)
    if inst[0] == "goto":
        return make_goto(inst, registers, labels)
    if inst[0] == "save":
        return make_save(inst, registers, stack)
    if inst[0] == "restore":
        return make_restore(inst, registers, stack)
    if inst[0] == "perform":
        return make_perform(inst, registers, ops, labels)

    raise Exception(f"unknown instruction type -- ASSEMBLE {inst}")  # pragma: no cover


def make_assign(inst, registers, ops, labels):
    # e.g. ["assign", "t", ...]
    reg_name = inst[1]
    value_exp = inst[2:]
    if value_exp[0][0] == "op":
        value_proc = make_operation_exp(value_exp, registers, ops, labels)
    else:
        value_proc = make_primitive_exp(value_exp[0], registers, labels)

    def proc():
        registers[reg_name] = value_proc()
        registers["pc"] += 1

    return proc


def make_primitive_exp(exp, registers, labels):
    keyword, value = exp
    if keyword == "const":  # ["const", 0]
        return lambda: value
    if keyword == "label":  # ["label", "loop"]
        idx = labels[value]
        return lambda: idx
    if keyword == "reg":  # ["reg", "n"]
        return lambda: registers[value]

    raise Exception(f"unknown expression type -- ASSEMBLE {exp}")  # pragma: no cover


def make_operation_exp(exp, registers, ops, labels):
    _, op_name = exp[0]
    op = ops[op_name]
    operands = exp[1:]
    aprocs = [make_primitive_exp(operand, registers, labels) for operand in operands]
    return lambda: op(*[proc() for proc in aprocs])


def make_test(inst, registers, ops, labels):
    condition = inst[1:]  # [["op", "="], ...
    condition_proc = make_operation_exp(condition, registers, ops, labels)

    def proc():
        registers["flag"] = condition_proc()
        registers["pc"] += 1

    return proc


def make_branch(inst, registers, labels):
    _, label = inst[1]  # ["label", "done"]
    idx = labels[label]

    def proc():
        if registers["flag"]:
            registers["pc"] = idx
        else:
            registers["pc"] += 1

    return proc


def make_goto(inst, registers, labels):
    dest = inst[1]

    if dest[0] == "label":  # ["goto", ["label", "test-b"]]
        label = dest[1]
        idx = labels[label]

        def proc():
            registers["pc"] = idx

        return proc

    if dest[0] == "reg":  # ["goto, ["reg", "continue"]]
        register_name = dest[1]

        def proc():
            registers["pc"] = registers[register_name]

        return proc


def make_save(inst, registers, stack):
    _, register_name = inst

    def proc():
        value = registers[register_name]
        stack.push(value)
        registers["pc"] += 1

    return proc


def make_restore(inst, registers, stack):
    _, register_name = inst

    def proc():
        value = stack.pop()
        registers[register_name] = value
        registers["pc"] += 1

    return proc


def make_perform(inst, registers, ops, labels):
    action = inst[1:]  # [["op", "print"], ...]
    action_proc = make_operation_exp(action, registers, ops, labels)

    def proc():
        action_proc()
        registers["pc"] += 1

    return proc
