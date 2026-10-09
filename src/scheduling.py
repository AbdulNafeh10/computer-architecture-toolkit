"""Conservative scheduling for adjacent load-use hazards."""
from .dependencies import LOADS, operands, hazards


def is_load(line):
    parts = line.strip().split(None, 1)
    return bool(parts) and parts[0].lower() in LOADS


def schedule(lines):
    """Fill a load-use gap with an independent ALU instruction if available."""
    result = list(lines)
    i = 0
    while i + 2 < len(result):
        dependency = hazards(result[i], result[i + 1])
        if is_load(result[i]) and dependency and 'RAW' in dependency:
            for j in range(i + 2, len(result)):
                candidate = result[j]
                if operands(candidate) is None or is_load(candidate):
                    break
                # Moving an instruction must not change any register dependencies.
                if any(hazards(candidate, other) or hazards(other, candidate)
                       for other in result[i:j]):
                    continue
                result.insert(i + 1, result.pop(j))
                break
        i += 1
    return result


def adjacent_load_hazards(lines):
    return [(i, i + 1) for i in range(len(lines) - 1)
            if is_load(lines[i]) and
            (hazards(lines[i], lines[i + 1]) or {}).get('RAW')]
