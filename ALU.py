from Memory import IH, Reg


class ALU:
    def add(self, op1, op2):
        a, b = self.hexTobin(op1), self.hexTobin(op2)
        lg = max(len(a), len(b))
        sm = ""
        bn = 0
        for i in range(lg - 1, -1, -1):
            rs = self.fullAdder(a[i], b[i], bn)
            sm = str(rs[0]) + sm
            bn = rs[1]
        sm = Reg(int(sm, 2))
        return sm, bn

    def sub(self, op1, op2):
        a, b = self.hexTobin(op1), self.hexTobin(op2)
        lg = max(len(a), len(b))
        sm = ""
        bn = 0
        for i in range(lg - 1, -1, -1):
            rs = self.fullSubtracter(a[i], b[i], bn)
            sm = str(rs[0]) + sm
            bn = rs[1]
        sm = Reg(int(sm, 2))
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
        if type(hx) is str:
            hx = int(hx, 16)
        idx = bin(hx).find("b")
        bins = bin(hx)[idx + 1:]
        return bins.rjust(64, "0")

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


if __name__ == "__main__":
    alu = ALU()
    print(alu.add("0x3333", "0x2222"))
