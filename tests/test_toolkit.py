import unittest
from src.preprocessing import preprocess, register_number
from src.dependencies import hazards, operands
from src.scheduling import schedule, adjacent_load_hazards


class ToolkitTests(unittest.TestCase):
    def test_registers(self):
        self.assertEqual(register_number('t0'), 5)
        self.assertEqual(register_number('x31'), 31)
        with self.assertRaises(ValueError):
            register_number('x32')

    def test_branch_offset(self):
        instructions, labels = preprocess('top: addi t0, t0, 1\nbeq t0, zero, top')
        self.assertEqual(labels, {'top': 0})
        self.assertEqual(instructions[1], ['beq', 5, 0, -4])

    def test_memory_normalization(self):
        inst, _ = preprocess('lw t0, 12(s1)\nsw t0, -4(s1)')
        self.assertEqual(inst, [['lw', 5, 9, 12], ['sw', 9, 5, -4]])

    def test_dependencies(self):
        self.assertEqual(hazards('add t0, t1, t2', 'sub t3, t0, t4'), {'RAW': ['x5']})
        self.assertEqual(hazards('add t0, t1, t2', 'add t1, t3, t4'), {'WAR': ['x6']})
        self.assertEqual(hazards('add t0, t1, t2', 'add t0, t3, t4'), {'WAW': ['x5']})
        self.assertEqual(hazards('add x5, x6, x7', 'add t1, t0, t2'), {'RAW': ['x5'], 'WAR': ['x6']})
        self.assertIsNone(operands('beq t0, t1, label'))

    def test_scheduling(self):
        lines = ['lw t0, 0(s1)', 'add t2, t0, t3', 'add t4, t5, t6']
        self.assertEqual(adjacent_load_hazards(lines), [(0, 1)])
        self.assertEqual(schedule(lines), [lines[0], lines[2], lines[1]])
        self.assertEqual(adjacent_load_hazards(schedule(lines)), [])

    def test_unknown_register_is_barrier(self):
        self.assertIsNone(operands('add t4, mystery, t2'))
        lines = ['lw t0, 0(s1)', 'add t2, t0, t3', 'add t4, mystery, t6']
        self.assertEqual(schedule(lines), lines)

    def test_aliases_and_zero_register(self):
        self.assertEqual(hazards('add x5, x6, x7', 'sub t1, t0, t3'),
                         {'RAW': ['x5'], 'WAR': ['x6']})
        self.assertEqual(hazards('add zero, t1, t2', 'add t3, zero, t4'), {})

    def test_no_crossing_write_or_memory(self):
        lines = ['lw t0, 0(s1)', 'add t2, t0, t3',
                 'add t4, t5, t6', 'sw t4, 0(s2)']
        self.assertEqual(schedule(lines)[1], lines[2])
        blocked = ['lw t0, 0(s1)', 'add t2, t0, t3',
                   'add t5, t1, t2', 'add t4, t5, t6']
        self.assertEqual(schedule(blocked), blocked)

    def test_no_unsafe_movement(self):
        lines = ['lw t0, 0(s1)', 'add t2, t0, t3', 'add t4, t2, t5']
        self.assertEqual(schedule(lines), lines)
        barrier = ['lw t0, 0(s1)', 'add t2, t0, t3', 'beq t4, t5, end', 'add t6, t1, t2']
        self.assertEqual(schedule(barrier), barrier)


if __name__ == '__main__':
    unittest.main()
