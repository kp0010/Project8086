class IH(int):
    def __repr__(self):
        lg = len(hex(self))
        return "0x" + hex(self)[2:].zfill(lg % 2 + lg - 2)

    def __add__(self, other):
        val = int(self) + int(other)
        return IH(val)

    def __sub__(self, other):
        val = int(self) - int(other)
        return IH(val)

    def __mul__(self, other):
        val = int(self) * int(other)
        return IH(val)


class Memory:
    def __init__(self, capacity):
        self.memory = bytearray(capacity)
        self.capacity = capacity

    def __getitem__(self, address):
        """Get the address and returns the value at that address"""
        if 0 <= address < self.capacity:
            return IH(self.memory[address])
        else:
            raise ValueError(f"Address {hex(address)} out of range")

    def __setitem__(self, address, byte):
        """Sets the value at the given address"""
        if 0 <= address < self.capacity:
            self.memory[address] = byte
        else:
            raise ValueError(f"Address {hex(address)} out of range")


if __name__ == '__main__':
    memory = Memory(2 ** 20)
    memory[0x10000] = 0b10100000
    print(memory[0x10000])
