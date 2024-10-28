import Lexer


class Instruction:
    def __init__(self, opcode, *oprands):
        self.opcode = opcode
        self.oprands = oprands

    def __repr__(self):
        return f"INS: {self.opcode.upper()} {self.oprands}"


class Binary:
    def __init__(self, left, operator, right):
        self.left = left
        self.right = right
        self.operator = operator

    def __repr__(self):
        return f"{self.left} {self.operator.lexeme} {self.right}"


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.curr = 0
        self.instructions = []

        while not self.isAtEnd():
            curr_ins = self.instruction()
            if curr_ins is not None:
                self.instructions.append(curr_ins)
            else:
                break

    # Grammer
    def instruction(self):
        operands = []
        opcode = None

        if self.matches("OPCODE",):
            opcode = self.opcode()

            while self.matches("REGISTER", "LEFT_BRACE", "NUMBER",
                               "COMMA", "IDENTIFIER"):
                prev = self.previous()
                if prev.tokenType != "COMMA":
                    term = self.term()
                    operands += [term]

        return Instruction(opcode, operands)

    def term(self):
        expr = self.factor()

        while self.matches("MINUS", "PLUS"):
            operator = self.previous()
            self.advance()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def factor(self):
        expr = self.primary()

        while self.matches("STAR"):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def primary(self):
        expr = self.previous()

        if expr.tokenType in ["NUMBER", "REGISTER", "IDENTIFIER"]:
            return expr.literal

        if expr.tokenType == "LEFT_BRACE":
            self.advance()
            expr = self.term()
            self.consume("RIGHT_BRACE", "EXPECT ] AFTER MEM")
            return expr

    def opcode(self):
        opcode = self.previous()
        return opcode.lexeme

    # Helpers
    def matches(self, *types):
        for tp in types:
            if self.checks(tp):
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
        return self.peek().tokenType == "EOF"

    def checks(self, tp):
        if self.isAtEnd():
            return False
        return self.peek().tokenType == tp

    def peek(self):
        return self.tokens[self.curr]

    def consume(self, tokenType, message):
        if self.checks(tokenType):
            return self.advance()

        raise ValueError(str(self.peek().literal) + message)


if __name__ == "__main__":
    lex = Lexer.Lexer()
    p = Parser(lex.tokens)
    # print("LEXED: ")
    # [print(x) for x in lex.tokens]
    print("\nPARSED: ")
    [print(x) for x in p.instructions]
