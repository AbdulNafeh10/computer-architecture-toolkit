`timescale 1ns / 1ns

module alu_testbench;
    reg [3:0] operation;
    reg signed [31:0] A, B;
    wire signed [31:0] ALUresult;

    alu uut (.operation(operation), .A(A), .B(B), .ALUresult(ALUresult));

    task check;
        input [3:0] code;
        input signed [31:0] left, right, expected;
        begin
            operation = code;
            A = left;
            B = right;
            #1;
            if (ALUresult !== expected) begin
                $display("FAIL op=%b A=%0d B=%0d got=%0d expected=%0d",
                         code, left, right, ALUresult, expected);
                $fatal(1);
            end
        end
    endtask

    initial begin
        check(4'b0010, 10, -5, 5);
        check(4'b0110, 10, -5, 15);
        check(4'b0111, 10, -5, -50);
        check(4'b1111, 10, -5, -2);
        check(4'b0100, 10, 2, 40);
        check(4'b1100, 10, 1, 5);
        check(4'b1110, -8, 1, -4);
        check(4'b0000, 10, 6, 2);
        check(4'b0001, 10, 6, 14);
        check(4'b0011, 10, 6, 12);
        check(4'b1000, 10, 10, 1);
        check(4'b1001, 10, 6, 1);
        check(4'b1010, -5, 10, 1);
        check(4'b1011, 10, -5, 1);
        check(4'b0101, 10, 6, 0);
        $display("ALU checks passed");
        $finish;
    end
endmodule
