from CPU import CPU8086
from Compiler import Lexer
from Compiler import Parser

cpu = CPU8086()

lexer = Lexer("./Compiler/test.asm")

parser = Parser(lexer.tokens)

[print(x) for x in parser.instructions]

cpu.Decoder.MOV("[0x00]", "ax")
cpu.MEMORY.displayMemory()

for ins in parser.instructions:
    print(ins.opcode, ins.operands)

    try:
        if (type(ins.operands[0]) is int):
            ins.operands[0] = "[" + str(ins.operands[0]) + "]"

        ins.operands[1] = "[" + str(ins.operands[1].resolve()) + "]"
        print(ins.operands[1])
    except (AttributeError, IndexError):
        ...

    if ins.opcode.upper() == "MOV":
        print(ins.operands)
        cpu.Decoder.MOV(ins.operands[0], ins.operands[1])
        cpu.displayReg()
        cpu.MEMORY.displayMemory(0x246)
    elif ins.opcode.upper() == "ADD":
        cpu.Decoder.ADD(ins.operands[0], ins.operands[1])
        cpu.displayReg()
    elif ins.opcode.upper() == "SUB":
        cpu.Decoder.SUB(ins.operands[0], ins.operands[1])
        cpu.displayReg()
    elif ins.opcode == "REG":
        cpu.displayReg()
    elif ins.opcode == "MEM":
        cpu.MEMORY.displayMemory(255)
        print("\n")
    elif ins.opcode == "HLT":
        print("EXITED")
        break
