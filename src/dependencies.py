"""Register read/write sets for the supported scheduling instructions."""
import re
from .preprocessing import register_number


def canonical(register):
    return f"x{register_number(register)}"


def active(registers):
    return {canonical(r) for r in registers} - {"x0"}


R_TYPE = {'add', 'sub', 'mul', 'div', 'and', 'or', 'xor', 'sll', 'srl', 'sra', 'slt'}
I_TYPE = {'addi', 'andi', 'ori', 'xori', 'slli', 'srli', 'srai', 'slti'}
LOADS = {'lb', 'lh', 'lw', 'lbu', 'lhu', 'ld'}
STORES = {'sb', 'sh', 'sw', 'sd'}


def operands(line):
    """Return (read registers, written registers) or None for barriers."""
    parts = [p for p in re.split(r'[,\s()]+', line.split('#', 1)[0].strip()) if p]
    if not parts:
        return None
    op = parts[0].lower()
    try:
        if op in R_TYPE and len(parts) == 4:
            return active([parts[2], parts[3]]), active([parts[1]])
        if op in I_TYPE and len(parts) == 4 and re.fullmatch(r'-?\d+', parts[3]):
            return active([parts[2]]), active([parts[1]])
        if op in LOADS and len(parts) == 4 and re.fullmatch(r'-?\d+', parts[2]):
            return active([parts[3]]), active([parts[1]])
    except ValueError:
        pass
    return None


def hazards(first, second):
    """Classify RAW, WAR and WAW register dependencies."""
    a, b = operands(first), operands(second)
    if a is None or b is None:
        return None
    reads_a, writes_a = a
    reads_b, writes_b = b
    found = {}
    for name, registers in [('RAW', writes_a & reads_b),
                            ('WAR', reads_a & writes_b),
                            ('WAW', writes_a & writes_b)]:
        if registers:
            found[name] = sorted(registers)
    return found
