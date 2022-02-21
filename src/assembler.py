def assemble(controller_text, machine):
    def receive(insts, labels):
        update_insts(insts, labels, machine)
        return insts

    return extract_labels(controller_text, receive)


def extract_labels(text, receive):
    if not text:
        return receive([], [])

    def new_receive(insts, labels):
        next_inst = text[0]
        if isinstance(next_inst, str):
            return receive(insts, [make_label_entry(next_inst, insts)] + labels)
        else:
            return receive([make_instruction(next_inst)] + insts, labels)

    return extract_labels(text[1:], new_receive)
