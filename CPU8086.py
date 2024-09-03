from Memory import Memory, IH, GenReg
from InstructionSet import *
from Decoder import Decoder

EXTBUS_SIZE = 20  # bits
INTBUS_SIZE = 16  # bits
MEMORY = Memory(2 ** EXTBUS_SIZE)
INSQ_SIZE = 6


class CPU8086:
    class BIU:
        def __init__(self, ExtAddrBus, InsQBus):
            # Segment Registers
            self.CS = IH(0x0000)
            self.DS = IH(0x2000)
            self.SS = IH(0x4000)
            self.ES = IH(0x6000)

            # Instruction Pointer
            self.IP = IH(0x0000)

            # 6 bytes Intruction Queue
            # self.insQ = insQ
            self.insQidx = 0
            self.insQ = [IH(0x00)] * 6
            self.InsQBus = InsQBus

            self.ExtAddrBus = ExtAddrBus

        def gen_phy_addr(self, segment, offset):
            self.ExtAddrBus = IH((segment << 4) + offset)

        def loadMemData(self, segment=None, offset=None, addr=None, word=False):
            if segment is None and offset is None:
                if addr is None:
                    self.ExtAddrBus = MEMORY[self.ExtAddrBus]
                    if word:
                        self.ExtAddrBus = (MEMORY[self.ExtAddrBus + 1] * (0x10 ** 2) +
                                           self.ExtAddrBus)
                else:
                    self.ExtAddrBus = MEMORY[addr]
                    if word:
                        self.ExtAddrBus = (MEMORY[addr + 1] * (0x10 ** 2) +
                                           self.ExtAddrBus)
            else:
                self.gen_phy_addr(segment, offset)
                self.ExtAddrBus = MEMORY[self.ExtAddrBus]
                if word:
                    self.ExtAddrBus = (MEMORY[self.ExtAddrBus + 1] * (0x10 ** 2) +
                                       self.ExtAddrBus)

            return self.ExtAddrBus

        def writeMemData(self, data, segment=None, offset=None, addr=None):
            if segment is None and offset is None:
                if addr is None:
                    MEMORY[self.ExtAddrBus] = data
                else:
                    MEMORY[addr] = data
            else:
                self.gen_phy_addr(segment, offset)
                MEMORY[self.ExtAddrBus] = data

        def fillQ(self):
            for idx in range(self.insQidx, INSQ_SIZE):
                # if self.insQ[idx] == 0x00:
                self.gen_phy_addr(self.CS, self.IP + idx + 1)
                self.insQ[idx] = self.loadMemData()

        def shiftQ(self, by=1):
            self.insQidx -= by
            for idx in range(INSQ_SIZE):
                if idx < INSQ_SIZE - by:
                    self.insQ[idx] = self.insQ[idx + by]
                else:
                    self.insQ[idx] = IH(0x00)

        def clearQ(self):
            self.insQidx = 0
            self.insQ = [IH(0x00)] * INSQ_SIZE

        def popQtoCSB(self):
            self.fillQ()
            ins = self.insQ[0]
            self.shiftQ()
            self.InsQBus = ins

    class EU:
        def __init__(self, InsQBus):
            # General Registers
            self.A = GenReg(0xAABB)
            self.B = GenReg(0xCCDD)
            self.C = GenReg(0x1122)
            self.D = GenReg(0x3344)

            # Index Registers
            self.SI = IH(0xAAAA)
            self.DI = IH(0xFFFF)
            self.BP = IH(0x0000)
            self.SP = IH(0x0000)

            # Flags
            self.CF = IH(0b0)
            self.PF = IH(0b0)
            self.AF = IH(0b0)
            self.ZF = IH(0b0)
            self.SF = IH(0b0)
            self.TF = IH(0b0)
            self.DF = IH(0b0)
            self.OF = IH(0b0)

            self.InsQBus = InsQBus

        def fetchDecodeIns(self):
            curIns = self.InsQBus

    def __init__(self):

        self.ExtAddrBus: hex = IH(0x00000)
        self.InsQBus = IH(0x00)
        self.insQ = [IH(0x00)] * INSQ_SIZE

        self.BIU = self.BIU(self.ExtAddrBus, self.InsQBus)
        self.EU = self.EU(self.InsQBus)

        self.Decoder = Decoder(self, MEMORY)


if __name__ == '__main__':
    cpu = CPU8086()

    MEMORY[0x22345] = 0xf1
    MEMORY[0x22346] = 0x1f

    # print(type(cpu.EU.regRef["A"]))
    # print(cpu.EU.A.X)
    # print(cpu.EU.A.H)
    # print(cpu.EU.A.L)
    # cpu.EU.regRef['A'].X = 0x1122
    # # cpu.EU.A.X = 0x1111f
    # print(cpu.EU.A.X)
    # print(cpu.EU.A.H)
    # print(cpu.EU.A.L)

    for i in range(0x0000, 0x100):
        cpu.BIU.writeMemData(data=0x0 + int(i), addr=i)

    # for i in range(0x0000, 0x100):
    #     print(cpu.BIU.loadMemData(addr=i, word=True))

    # MEMORY.displayMemory(0x50, index=1)

    print(cpu.EU.A.X, cpu.EU.B.X)
    cpu.Decoder.MOV("AX", "0x9999")
    print(cpu.EU.A.X, cpu.EU.B.X)

    # print(cpu.BIU.insQ)
    # cpu.BIU.fillQ()
    # print(cpu.BIU.insQ)
    # cpu.BIU.shiftQ(by=3)
    # cpu.BIU.IP += 3
    # print(cpu.BIU.insQ)
    # cpu.BIU.fillQ()
    # print(cpu.BIU.insQ)
    # cpu.BIU.clearQ()
    # print(cpu.BIU.insQ)
    # cpu.BIU.IP += 244
    # cpu.BIU.fillQ()
    # print(cpu.BIU.insQ)

    # print(cpu.BIU.loadMemData(cpu.BIU.DS, 0x2345))
    # print(MEMORY[cpu.BIU.gen_phy_addr(cpu.BIU.DS, 0x2346)])
