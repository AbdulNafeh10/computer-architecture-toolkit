"""Basic preprocessing for a small subset of RISC-V assembly."""
import re

ABI = dict(zip(
    'zero ra sp gp tp t0 t1 t2 s0 s1 a0 a1 a2 a3 a4 a5 a6 a7 s2 s3 s4 s5 s6 s7 s8 s9 s10 s11 t3 t4 t5 t6'.split(),
    range(32),
))
ABI['fp'] = 8
MEMORY = {'lb', 'lh', 'lw', 'lbu', 'lhu', 'ld', 'sb', 'sh', 'sw', 'sd'}


def register_number(name):
    if name in ABI:
        return ABI[name]
    if re.fullmatch(r'x(?:[0-9]|[12][0-9]|3[01])', name):
        return int(name[1:])
    raise ValueError(f'Unknown register: {name}')


def preprocess(source):
    """Return (tokenized instructions, byte-addressed labels).

    Branch label operands become offsets relative to their instruction address.
    Tokens of memory instructions are normalized to [op, reg, base, offset]
    for loads or [op, base, reg, offset] for stores.
    """
    instructions, labels = [], {}
    for original in source.splitlines():
        line = original.split('#', 1)[0].strip()
        if not line:
            continue
        while ':' in line:
            name, rest = line.split(':', 1)
            name = name.strip()
            if not re.fullmatch(r'[A-Za-z_]\w*', name):
                raise ValueError(f'Invalid label: {name}')
            if name in labels:
                raise ValueError(f'Duplicate label: {name}')
            labels[name] = len(instructions) * 4
            line = rest.strip()
        if line:
            instructions.append([s for s in re.split(r'[,\s()]+', line) if s])
    for index, parts in enumerate(instructions):
        op = parts[0]
        if op in MEMORY and len(parts) == 4:
            if op[0] == 's':
                parts[:] = [op, parts[3], parts[1], parts[2]]
            else:
                parts[:] = [op, parts[1], parts[3], parts[2]]
        for i in range(1, len(parts)):
            token = parts[i]
            if token in labels:
                parts[i] = labels[token] - index * 4
            elif token in ABI or re.fullmatch(r'x(?:[0-9]|[12][0-9]|3[01])', token):
                parts[i] = register_number(token)
            elif re.fullmatch(r'-?\d+', token):
                parts[i] = int(token)
    return instructions, labels
