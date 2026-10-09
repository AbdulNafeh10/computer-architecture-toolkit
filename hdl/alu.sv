`timescale 1ns / 1ns

module alu(
    input signed [3:0] operation,
    input signed [31:0] A,
    input signed [31:0] B,
    output reg signed [31:0] ALUresult
);

    always @(*) begin
        case(operation)
            4'b0010: ALUresult = A + B;
            4'b0110: ALUresult = A - B;
            4'b0111: ALUresult = A * B;
            4'b1111: ALUresult = A / B;
            4'b0100: ALUresult = A << B;
            4'b1100: ALUresult = A >> B;
            4'b1110: ALUresult = A >>> B;
            4'b0000: ALUresult = A & B;
            4'b0001: ALUresult = A | B;
            4'b0011: ALUresult = A ^ B;
            4'b1000: ALUresult = (A == B) ? 1 : 0;
            4'b1001: ALUresult = (A != B) ? 1 : 0;
            4'b1010: ALUresult = (A < B) ? 1 : 0;
            4'b1011: ALUresult = (A >= B) ? 1 : 0;
            default: ALUresult = 0;
        endcase
    end

endmodule
