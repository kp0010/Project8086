from Memory import Memory, IH, GenReg
from InstructionSet import *

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
            self.insQ = insQ

            self.ExtAddrBus = ExtAddrBus
            self.InsQBus = InsQBus

        def gen_phy_addr(self, segment, offset):
            self.ExtAddrBus = IH((segment << 4) + offset)

        def loadMemData(self, segment=None, offset=None, addr=None):
            if segment is None and offset is None:
                if addr is None:
                    self.ExtAddrBus = MEMORY[self.ExtAddrBus]
                else:
                    self.ExtAddrBus = MEMORY[addr]
            else:
                self.gen_phy_addr(segment, offset)
                self.ExtAddrBus = MEMORY[self.ExtAddrBus]

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
            for idx in range(INSQ_SIZE):
                if self.insQ[idx] == 0x00:
                    self.gen_phy_addr(self.CS, self.IP + idx + 1)
                    self.insQ[idx] = self.loadMemData()

        def shiftQ(self, by=1):
            for idx in range(INSQ_SIZE):
                if idx < INSQ_SIZE - by:
                    self.insQ[idx] = self.insQ[idx + by]
                else:
                    self.insQ[idx] = IH(0x00)

        def clearQ(self):
            self.insQ = [IH(0x00)] * INSQ_SIZE

        def popQtoCSB(self):
            self.fillQ()
            ins = self.insQ[0]
            self.shiftQ()
            self.InsQBus = ins

    class EU:
        def __init__(self, InsQBus):
            # General Registers
            self.AX, self.AH, self.AL = GenReg(0xAABB).allot()
            self.BX, self.BH, self.BL = GenReg(0xCCDD).allot()
            self.CX, self.CH, self.CL = GenReg(0x1122).allot()
            self.DX, self.DH, self.DL = GenReg(0x3344).allot()

            # Index Registers
            self.SI = IH(0x0000)
            self.DI = IH(0x0000)
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


if __name__ == '__main__':
    cpu = CPU8086()

    # print(cpu.EU.AH)
    # cpu.EU.AH = IH(0xff)
    # print(cpu.EU.AX)
    # print(cpu.EU.AH, cpu.EU.AX, cpu.EU.AL)
    # print(cpu.EU.AH, cpu.EU.AX + cpu.EU.AH)
    # new = cpu.EU.AH + cpu.EU.AL
    #  print(new + cpu.EU.AL)

    MEMORY[0x22345] = 0xf1
    MEMORY[0x22346] = 0x1f

    for i in range(0x0000, 0x0010):
        cpu.BIU.writeMemData(data=0xa0 + int(i), addr=i)

    print(cpu.BIU.insQ)
    cpu.BIU.fillQ()
    print(cpu.BIU.insQ)
    cpu.BIU.shiftQ(by=3)
    cpu.BIU.IP += 3
    print(cpu.BIU.insQ)
    cpu.BIU.fillQ()
    print(cpu.BIU.insQ)
    # cpu.BIU.clearQ()
    # print(cpu.BIU.insQ)

    print(cpu.BIU.loadMemData(cpu.BIU.DS, 0x2345))
    # print(MEMORY[cpu.BIU.gen_phy_addr(cpu.BIU.DS, 0x2346)])
