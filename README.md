# Computer Architecture Toolkit

A small RISC-V instruction analysis and scheduling project built from earlier computer architecture coursework. It parses basic assembly, checks register dependencies, and moves independent instructions to reduce adjacent load-use hazards. The repository also includes RISC-V assembly examples and two SystemVerilog hardware modules.

## Scheduling example

A load followed immediately by an instruction that uses its result can stall a simple pipeline. The scheduler looks for an independent instruction to fill that gap.

**Before**

```asm
lw  t0, 0(s1)
add t2, t0, t3
add t4, t5, t6
```

**After**

```asm
lw  t0, 0(s1)
add t4, t5, t6
add t2, t0, t3
```

Adjacent load-use hazards in this example: **1 -> 0**. This is an instruction-order example, not a measured clock-cycle performance claim.

Run the example from the repository root:

```bash
python demo.py
```

## What's included

- `src/preprocessing.py`: labels, branch offsets, memory operands and numeric registers.
- `src/dependencies.py`: RAW, WAR and WAW register checks for supported instructions.
- `src/scheduling.py`: conservative local scheduling; stops at branches, stores, labels and unsupported instructions.
- `examples/`: runnable scheduler input and recovered assembly examples.
- `hdl/`: recovered SystemVerilog ALU and Control Unit designs with testbenches.
- `tests/`: checks for Python preprocessing, dependencies and safe instruction movement.

## Tests

```bash
python -m unittest discover -s tests -v
```

The Python tests can be run with the command above. HDL testbenches check expected outputs, but simulation has not been run in this environment. No waveform or performance results are claimed.

## Scope

This is a teaching-scale instruction tool, not a complete assembler, simulator or compiler. Scheduling supports a limited set of RISC-V operations and deliberately avoids moving instructions when it cannot establish safety. The code originated in collaborative CDA 4205L coursework with Joshua Vrana and was later reorganized and extended for this repository; individual contributions to the original files have not been established.
