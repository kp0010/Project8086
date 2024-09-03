from Memory import IH


class ALU:
    def ADD(self, op1, op2):
        print(self.bitwiseAdder(op1, op2))

    def bitwiseAdder(self, op1, op2):
        a, b = self.hexTobin(op1), self.hexTobin(op2)
        print(a, b)
        lg = max(len(a), len(b))
        sm = ""
        bn = 0
        for i in range(lg - 1, -1, -1):
            rs = self.fullAdder(a[i], b[i], bn)
            sm = str(rs[0]) + sm
            bn = rs[1]
        return sm, bn

    def bitwiseSubtractor(self, op1, op2):
        a, b = self.hexTobin(op1), self.hexTobin(op2)
        print(a, b)
        lg = max(len(a), len(b))
        sm = ""
        bn = 0
        for i in range(lg - 1, -1, -1):
            rs = self.fullSubtracter(a[i], b[i], bn)
            sm = str(rs[0]) + sm
            bn = rs[1]
            print(sm, bn)
        return sm, bn

    def fullAdder(self, a, b, cin):
        a = int(a)
        b = int(b)
        return (a ^ b) ^ cin, ((a ^ b) & cin) | (a & b)

    def fullSubtracter(self, a, b, brin):
        a = int(a)
        b = int(b)
        return (a ^ b) ^ brin, (~(a ^ b) & brin) | (~a & b)

    def hexTobin(self, hx):
        mp = [8, 16, 32, 64]
        idx = bin(hx).find("b")
        bins = bin(hx)[idx + 1:]
        lbin = (len(bins) - 1) // 8
        return bins.rjust(mp[lbin], "0")

    def twosComplement(self, bn):
        comp = ""
        flg = False
        for i in bn[::-1]:
            if not flg:
                if i == "0":
                    comp = i + comp
                else:
                    flg = True
                    comp = i + comp
            else:
                comp = ("0" if i == "1" else "1") + comp
        return comp

    # ADD(IH(0xF0), IH(0x0f))
    # print(x := bitwiseSubtractor(IH(0b01010101), IH(0b10101010)))
alu = ALU()
print(x := alu.bitwiseAdder(IH(0b11100000), IH(0b11100000)))
print(y := alu.twosComplement(str(x[0])))
print(x[0], y, type(x[0]))
print(int(0xf), int(0x1f))
print(int(x[0], 2))
print(int(y, 2))
