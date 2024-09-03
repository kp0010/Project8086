from InstructionSet import InstructionSet
from Memory import Memory, IH, GenReg


class Decoder:
    def __init__(self, CPU, MEMORY: Memory):
        self.InstructionSet = InstructionSet
        self.CPU = CPU
        self.MEMORY = MEMORY

    def getSrc(self, loc):
        if hasattr(self.CPU.EU, loc):
            return getattr(self.CPU.EU, loc)
        elif hasattr(self.CPU.BIU, loc):
            return getattr(self.CPU.BIU, loc)
        elif hasattr(self.CPU.EU, loc[0]):
            return getattr(getattr(self.CPU.EU, loc[0]), loc[-1])
        # else:
            # raise AttributeError(f"{loc} Location not found")

    def setDst(self, loc, val):
        if hasattr(self.CPU.EU, loc):
            setattr(self.CPU.EU, loc, val)
        elif hasattr(self.CPU.BIU, loc):
            setattr(self.CPU.BIU, loc, val)
        elif hasattr(self.CPU.EU, loc[0]):
            setattr(getattr(self.CPU.EU, loc[0]), loc[-1], val)
        # else:
            # raise AttributeError(f"{loc} Location not found")

    def LOAD(self, src, dst):
        self.setDst(dst, self.getSrc(src))
