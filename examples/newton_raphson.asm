.data

.text
    li t0, 100500
    fcvt.s.w fa0, t0
    jal prntFloat
    fsqrt.s fa0, fa0
    jal prntFloat
    fmul.s fa0, fa0, fa0
    jal prntFloat
    jal prntNewLine

    fcvt.d.w fa0, t0
    jal prntDouble
    fsqrt.d fa0, fa0
    jal prntDouble
    fmul.d fa0, fa0, fa0
    jal prntDouble
    jal prntNewLine

    # Newton-Raphson uses a change below 1e-8 as the stopping point.
    li t5, 100000000
    li t6, 1
    fcvt.d.w ft9, t5
    fcvt.d.w ft11, t6
    fdiv.d ft9, ft11, ft9

    li t1, 1423
    li t2, 2
    li t3, 10
    fcvt.d.w ft0, t1
    fcvt.d.w ft2, t2
    fcvt.d.w ft4, t3

    jal NewtonRoots
    fmv.d fa0, ft10
    jal prntNewLine
    jal prntDouble
    jal exit

NewtonRoots:
    flt.d t4, ft0, ft4
    beqz t4, morethan10
    fdiv.d ft5, ft0, ft2
    j endif
morethan10:
    fdiv.d ft5, ft0, ft4
endif:
NewtonRootsLoop:
    fmv.d ft8, ft5
    fmul.d ft6, ft5, ft5
    fsub.d ft6, ft6, ft0
    fmul.d ft7, ft5, ft2
    fdiv.d ft6, ft6, ft7
    fsub.d ft5, ft5, ft6

    # Compare the new approximation with the previous one.
    fsub.d ft7, ft8, ft5
    fabs.d ft7, ft7
    fle.d t6, ft7, ft9
    bnez t6, end
    j NewtonRootsLoop
end:
    fmv.d ft10, ft5
    jr ra

prntFloat:
    li a7, 2
    ecall
    li a0, '\n'
    li a7, 11
    ecall
    jr ra

prntDouble:
    li a7, 3
    ecall
    li a0, '\n'
    li a7, 11
    ecall
    jr ra

prntNewLine:
    li a0, '\n'
    li a7, 11
    ecall
    jr ra

exit:
    li a7, 10
    ecall
