from InstructionSet import InstructionSet
from Memory import Memory, IH, GenReg


class Decoder:
    def __init__(self, CPU, MEMORY: Memory):
        self.InstructionSet = InstructionSet
        self.CPU = CPU
        self.MEMORY = MEMORY

        self.regRef = {
            'AX': CPU.EU.A.X, 'AL': CPU.EU.A.L, 'AH': CPU.EU.A.H,
            'BX': CPU.EU.B.X, 'BL': CPU.EU.B.L, 'BH': CPU.EU.B.H,
            'CX': CPU.EU.C.X, 'CL': CPU.EU.C.L, 'CH': CPU.EU.C.H,
            'DX': CPU.EU.D.X, 'DL': CPU.EU.D.L, 'DH': CPU.EU.D.H,
            'SI': CPU.EU.SI, 'DI': CPU.EU.DI,
            'BP': CPU.EU.BP, 'SP': CPU.EU.SP,
            'CS': CPU.BIU.CS, 'DS': CPU.BIU.DS,
            'SS': CPU.BIU.SS, 'ES': CPU.BIU.ES,
            'IP': CPU.BIU.IP
        }

    def getSrc(self, loc):
        if hasattr(self.CPU.EU, loc):
            return getattr(self.CPU.EU, loc)
        elif hasattr(self.CPU.BIU, loc):
            return getattr(self.CPU.BIU, loc)

    def setDst(self, loc, val):
        if hasattr(self.CPU.EU, loc):
            setattr(self.CPU.EU, loc, val)
        if hasattr(self.CPU.BIU, loc):
            setattr(self.CPU.BIU, loc, val)

    def LOAD(self, src, dst):
        self.setDst(dst, self.getSrc(src))
