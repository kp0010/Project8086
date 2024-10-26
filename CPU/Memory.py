class IH(int):
    def __repr__(self):
        lg = len(hex(self)) - 2
        return "0x" + "0" * (2-lg) + hex(self)[2:]

    def __str__(self):
        lg = len(hex(self)) - 2
        return "0x" + "0" * (2-lg) + hex(self)[2:]

    def __add__(self, other):
        val = int(self) + int(other)
        return IH(val)

    def __sub__(self, other):
        val = int(self) - int(other)
        return IH(val)

    def __mul__(self, other):
        val = int(self) * int(other)
        return IH(val)


class Reg(IH):
    def __repr__(self):
        lg = len(hex(self)) - 2
        return "0x" + "0" * (4-lg) + hex(self)[2:]

    def __str__(self):
        lg = len(hex(self)) - 2
        return "0x" + "0" * (4-lg) + hex(self)[2:]


class GenReg:
    def __init__(self, value):
        self._X = Reg(value)

    @ property
    def H(self): return Reg((0xFF00 & self._X) >> 8)

    @ H.setter
    def H(self, value): self._X = Reg((value * (16 ** 2)) + (self._X & 0xFF))

    @ property
    def L(self): return Reg((0x00FF & self._X))

    @ L.setter
    def L(self, value): self._X = Reg(value + (self._X & 0xFF00))

    @ property
    def X(self): return self._X

    @ X.setter
    def X(self, value): self._X = Reg(value)

    def allot(self):
        return self.X, self.H, self.L


class Memory:
    def __init__(self, capacity):
        self.memory = bytearray(capacity)
        self.capacity = capacity

    def __getitem__(self, address):
        """Get the address and returns the value at that address"""
        address = int(address, 16)
        if 0 <= address < self.capacity:
            return IH(self.memory[address])
        else:
            raise ValueError(f"Address {hex(address)} out of range")

    def __setitem__(self, address, byte):
        """Sets the value at the given address"""
        if type(address) is not int:
            address = int(address, 16)
        if 0 <= address < self.capacity:
            self.memory[address] = byte
        else:
            raise ValueError(f"Address {hex(address)} out of range")

    def displayMemory(self, start=None, end=None, index=False):
        """Displays the memory contents fully or some section"""
        if index:
            print("xxxxx:  ", end="")
            [print(f"{str(IH(x))[2:]}{' -' if x == 0x07 else ''}", end=" ")
             for x in range(0x10)]
            print("\n", end='')
        start = 0x00 if start is None else start // 16 * 16
        end = start + 0x5f if end is None else end
        startFlag = True
        for idx in range(start, end+1):
            if idx % 0x10 == 0:
                if not startFlag:
                    print("\n", end="")
                startFlag = False
                print(f"{str(hex(idx))[2:].rjust(5, "0")}", end=":  ")
            ends = " - " if not (idx + 1) % 0x08 and (idx + 1) % 0x10 else " "
            print(str(IH(self.memory[idx]))[2:], end=ends)


if __name__ == '__main__':
    memory = Memory(2 ** 20)
    # memory.displayMemory()

    R = GenReg(0x1122)
    print(R.X)
    print(R.H)

    R.L = 0x44
    print(R.H)
    print(R.X)
