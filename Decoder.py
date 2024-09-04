from InstructionSet import InstructionSet
from Memory import Memory, IH, GenReg, Reg


class Decoder:
    def __init__(self, CPU, MEMORY: Memory, ALU):
        self.InstructionSet = InstructionSet
        self.CPU = CPU
        self.MEMORY = MEMORY
        self.ALU = ALU

    def getSrc(self, loc, byt=2):
        loc = loc.upper()
        if hasattr(self.CPU.EU, loc):
            return getattr(self.CPU.EU, loc)
        elif hasattr(self.CPU.BIU, loc):
            return getattr(self.CPU.BIU, loc)
        elif hasattr(self.CPU.EU, loc[0]):
            return getattr(getattr(self.CPU.EU, loc[0]), loc[-1])
        elif '0X' == loc[:2]:
            return IH(int(loc, 16))
        elif (loc[0], loc[-1]) == ("[", "]"):
            loc = loc[1:-1].lower()
            if byt == 2:
                return int(str(self.MEMORY[hex(int(loc, 16) + 1)]) + str(self.MEMORY[loc])[2:], 16)
            else:
                return int(self.MEMORY[loc])
        else:
            raise AttributeError(f"{loc} Location not found")

    def setDst(self, loc, val, byt=2):
        loc = loc.upper()
        if hasattr(self.CPU.EU, loc):
            setattr(self.CPU.EU, loc, val)
        elif hasattr(self.CPU.BIU, loc):
            setattr(self.CPU.BIU, loc, val)
        elif hasattr(self.CPU.EU, loc[0]):
            setattr(getattr(self.CPU.EU, loc[0]), loc[-1], val)
        elif (loc[0], loc[-1]) == ('[', ']'):
            loc = int(loc.lower()[1:-1], 16)
            x = int(hex(val)[-2:], 16)
            self.MEMORY[loc] = x
            if byt == 2:
                y = int(hex(val)[2:-2], 16)
                self.MEMORY[loc + 1] = y
        else:
            raise AttributeError(f"{loc} Location not found")

    def MOV(self, op1, op2):
        op1, op2 = op1.upper(), op2.upper()
        bytd = 2
        byts = 2
        if op1[-1] in "HL":
            if op2[-1] not in "HL]":
                raise ValueError("Operand Size Does not match")
            if op2[-1] == ']':
                bytd = 1
        if op2[-1] in "HL":
            if op1[-1] not in "HL]":
                raise ValueError("Operand Size Does not match")
            if op1[-1] == ']':
                byts = 1
        val = self.getSrc(op2, byt=byts)
        self.setDst(op1, val, byt=bytd)

    def ADD(self, op1, op2):
        op1, op2 = op1.upper(), op2.upper()
        op1val = self.getSrc(op1)
        op2val = self.getSrc(op2)
        sum_res = self.ALU.add(op1=op1val, op2=op2val)
        self.CPU.EU.CF = IH(sum_res[1])
        self.setDst(op1, sum_res[0])

    def SUB(self, op1, op2):
        op1, op2 = op1.upper(), op2.upper()
        op1val = self.getSrc(op1)
        op2val = self.getSrc(op2)
        sub_res = self.ALU.sub(op1=op1val, op2=op2val)
        self.CPU.EU.SF = IH(sub_res[1])
        self.setDst(op1, sub_res[0])
