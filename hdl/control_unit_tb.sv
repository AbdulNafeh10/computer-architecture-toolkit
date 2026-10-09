`timescale 1ns / 1ns

module cu_testbench;
    reg [6:0] opcode;
    wire ALUSrc, MemtoReg, RegWrite, MemRead, MemWrite, Branch, Jump, Jalr;
    wire [1:0] ALUOp;

    cu uut (.opcode(opcode), .ALUSrc(ALUSrc), .MemtoReg(MemtoReg),
            .RegWrite(RegWrite), .MemRead(MemRead), .MemWrite(MemWrite),
            .Branch(Branch), .Jump(Jump), .Jalr(Jalr), .ALUOp(ALUOp));

    task check;
        input [6:0] code;
        input [9:0] expected;
        begin
            opcode = code;
            #1;
            if ({ALUSrc, MemtoReg, RegWrite, MemRead, MemWrite,
                 Branch, Jump, Jalr, ALUOp} !== expected) begin
                $display("FAIL opcode=%b", code);
                $fatal(1);
            end
        end
    endtask

    initial begin
        check(7'b0110011, 10'b0010000010); // R-type
        check(7'b0000011, 10'b1111000000); // load
        check(7'b1100111, 10'b1010001100); // jalr
        check(7'b0010011, 10'b1010000010); // immediate
        check(7'b0100011, 10'b1000100000); // store
        check(7'b1100011, 10'b0000010001); // branch
        check(7'b1101111, 10'b0010001000); // jump
        check(7'b1111111, 10'b0000000000); // unsupported
        $display("Control Unit checks passed");
        $finish;
    end
endmodule
