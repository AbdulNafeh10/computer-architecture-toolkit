"""Show a before-and-after scheduling example."""
from pathlib import Path
from src.scheduling import schedule, adjacent_load_hazards

original = [line.strip() for line in Path('examples/hazard.asm').read_text().splitlines()
            if line.strip() and not line.lstrip().startswith('#')]
updated = schedule(original)

for heading, code in [('Before', original), ('After', updated)]:
    print(f'{heading} ({len(adjacent_load_hazards(code))} adjacent load-use hazards):')
    for line in code:
        print(f'  {line}')
    print()
