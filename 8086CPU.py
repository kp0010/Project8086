from Memory import Memory, IH

EXTBUS_SIZE = 20  # bits
INTBUS_SIZE = 16  # bits
MEMORY = Memory(2 ** EXTBUS_SIZE)
INSQ_SIZE = 6


class GenReg:
    def __init__(self, value):
        self.X = IH(value)
        self.H = IH(0xFF00 & self.X >> 8)
        self.L = IH(0x00FF & self.X)

    def allot(self):
        return self.X, self.H, self.L


class CPU8086:
    class BIU:
        def __init__(self, CPU):
            self.CPU8086 = CPU

            # Segment Registers
            self.CS = IH(0x0000)
            self.DS = IH(0x2000)
            self.SS = IH(0x4000)
            self.ES = IH(0x6000)

            # Instruction Pointer
            self.IP = IH(0x0000)

            # 6 bytes Intruction Queue
            self.insQ = [IH(0x00)] * INSQ_SIZE

            self.controlSysBus = IH(0x00)

        def gen_phy_addr(self, segment, offset):
            return (segment << 4) + offset

        def fillQ(self):
            for idx in range(INSQ_SIZE):
                if self.insQ[idx] == 0x00:
                    self.insQ[idx] = MEMORY[self.gen_phy_addr(self.CS, self.IP + idx + 1)]

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
            controlSystemBus = ins

    class EU:
        def __init__(self, CPU):
            self.CPU8086 = CPU

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

        def execute(self):
            pass

    def __init__(self):
        global MEMORY

        self.ExtAddrBus: hex = 0x00000

        self.BIU = self.BIU(self)
        self.EU = self.EU(self)


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
        MEMORY[cpu.BIU.gen_phy_addr(cpu.BIU.CS, i)] = 0xa0 + int(i)

    print(cpu.BIU.insQ)
    cpu.BIU.fillQ()
    print(cpu.BIU.insQ)
    cpu.BIU.shiftQ(by=3)
    cpu.BIU.IP += 3
    print(cpu.BIU.insQ)
    cpu.BIU.fillQ()
    print(cpu.BIU.insQ)
    cpu.BIU.clearQ()
    print(cpu.BIU.insQ)

    print(MEMORY[cpu.BIU.gen_phy_addr(cpu.BIU.DS, 0x2345)])
    print(MEMORY[cpu.BIU.gen_phy_addr(cpu.BIU.DS, 0x2346)])
