import Lexer


class Instruction:
    def __init__(self, opcode, *oprands):
        self.opcode = opcode
        self.oprands = oprands


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.curr = 0
        print(self.tokens)

    def instruction(self):
        opcode = self.opcode()

        operands = []
        while self.matches("REGISTER", "MEMORY", "IMMEDIATE", "COMMA"):
            prev = self.previous()
            if prev.tokenType != "COMMA":
                operands += prev

        return Instruction(opcode, operands)

    def oprands(self):
        return

    def matches(self, *types):
        for tp in types:
            if self.checks(type):
                self.advance()
                return True
        return False

    def advance(self):
        if not self.isAtEnd():
            self.curr += 1
        return self.previous()

    def previous(self):
        return self.tokens[self.curr - 1]

    def isAtEnd(self):
        return not self.curr < len(self.tokens)

    def checks(self, type):
        if self.isAtEnd():
            return False
        return self.peek().tokenType == type

    def peek(self):
        return self.tokens[self.curr]


if __name__ == "__main__":
    lex = Lexer.Lexer()
    Parser(lex.tokens)
