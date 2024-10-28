class Token:
    def __init__(self, tokenType, lexeme, literal, line):
        self.tokenType = tokenType
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __repr__(self):
        return f"{self.tokenType} {self.lexeme} {self.literal}"


class Lexer:
    def __init__(self):
        self.file_name = "./test.asm"

        self.start = 0
        self.curr = 0
        self.line = 0

        self.opcodes = [
            'MOV', 'PUSH', 'POP', 'XCHG',
            'ADD', 'SUB', 'MUL', 'DIV', 'INC', 'DEC',
            'AND', 'OR', 'XOR', 'NOT',
            'JMP', 'CALL', 'RET', 'JZ', 'JNZ',
            'CMP', 'TEST',
            'MOVS', 'CMPS', 'SCAS', 'LODS',
            'IN', 'OUT',
            'CLC', 'STC', 'CLI', 'STI',
            'NOP', 'HLT'
        ]

        self.registers = [
            "AX", "AL", "AH",
            "BX", "BL", "BH",
            "CX", "CL", "CH",
            "DX", "DL", "DH",
            "SI", "DI", "SP", "BP"
            "CS", "DS", "ES", "SS", "IP"
        ]

        self.tokens = []

        self.source = self.read_file()

        self.errors = []

        self.scanTokens()

    def read_file(self):
        with open(self.file_name, "r") as asm:
            contents = " ".join(asm.readlines())
            return contents

    def scanTokens(self):
        while not self.isAtEnd():
            self.start = self.curr
            self.scanToken()

        self.tokens.append(Token("EOF", "", None, self.line))

    def scanToken(self):
        char = self.advance()
        match char:
            case '(':
                self.addToken("LEFT_PAREN")
            case ')':
                self.addToken("RIGHT_PAREN")
            case '[':
                # self.addMem()
                self.addToken("LEFT_BRACE")
            case ']':
                self.addToken("RIGHT_BRACE")
            case '{':
                self.addToken("LEFT_CBRACE")
            case '}':
                self.addToken("RIGHT_CBRACE")
            case ',':
                self.addToken("COMMA")
            case '.':
                self.addToken("DOT")
            case '-':
                self.addToken("MINUS")
            case '+':
                self.addToken("PLUS")
            case ';':
                while self.peek() != '\n' and not self.isAtEnd():
                    self.advance()
            case '*':
                self.addToken("STAR")
            case '!':
                self.addToken("BANG_EQUAL" if self.matchN('=') else "BANG")
            case '=':
                self.addToken("EQUAL_EQUAL" if self.matchN('=') else "EQUAL")
            case '<':
                self.addToken("LESS_EQUAL" if self.matchN('=') else "LESS")
            case '>':
                self.addToken("GREATER_EQUAL" if self.matchN('=')
                              else "GREATER")
            case '"':
                self.addString()
            case char if char.isdigit():
                self.addNum()
            case char if char.isalpha():
                self.addIdentifier()
            case ' ' | '\r' | '\t':
                ...
            case '\n':
                self.line += 1
            case _:
                self.logError(self.line, f"Unexpected Char {char}")

    def advance(self):
        self.curr += 1
        return self.source[self.curr - 1]

    def matchN(self, exp):
        if self.isAtEnd():
            return False
        if self.source[self.curr] != exp:
            return False

        self.curr += 1
        return True

    def peek(self):
        if self.isAtEnd():
            return '\0'
        return self.source[self.curr]

    def addIdentifier(self):
        while self.peek().isalnum():
            self.advance()

        txt = self.source[self.start: self.curr]
        if txt.upper() in self.opcodes:
            self.addToken("OPCODE")
            return
        if txt.upper() in self.registers:
            self.addToken("REGISTER", txt.upper())
            return
        self.addToken("IDENTIFIER", txt)

    def addString(self):
        while self.peek() != '"' and not self.isAtEnd():
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if self.isAtEnd():
            self.logError(self.line, "EOF String")
            return

        self.advance()

        val = self.source[self.start + 1: self.curr - 1]
        self.addToken("STRING", val)

    def ishex(self, char):
        if char.isdigit():
            return True
        if 'a' <= char.lower() <= 'f':
            return True
        return False

    def addNum(self):
        hexn = False
        while self.peek().isdigit():
            self.advance()

        if self.peek() == 'x' and self.ishex(self.peekNext()):
            self.advance()
            hexn = True

        while self.ishex(self.peek()):
            self.advance()

        num = self.source[self.start: self.curr]
        if hexn:
            num = int(num, 16)
        else:
            num = int(num)

        self.addToken("NUMBER", num)

    def addMem(self):
        hexn = False
        while self.peek().isdigit():
            self.advance()

        if self.peek() == 'x' and self.ishex(self.peekNext()):
            self.advance()
            hexn = True

        while self.ishex(self.peek()):
            self.advance()

        if self.peek() != ']':
            self.logError(self.line, "Incorrect Memory Location")
        else:
            self.advance()

        num = self.source[self.start + 1: self.curr - 1]
        if hexn:
            num = int(num, 16)
        else:
            num = int(num)

        self.addToken("MEMORY", num)

    def peekNext(self):
        if self.curr + 1 >= len(self.source):
            return "\0"
        return self.source[self.curr + 1]

    def isAtEnd(self):
        return self.curr >= len(self.source)

    def addToken(self, tokenType, literal=None):
        text = self.source[self.start: self.curr]
        self.tokens.append(Token(tokenType, text, literal, self.line))

    def logError(self, line, error):
        self.errors.append(f"err at {line}: {error}")


if __name__ == "__main__":
    lx = Lexer()
    print("LEXED: ")
    [print(x) for x in lx.tokens]
