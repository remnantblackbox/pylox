from token_type import TokenType
from token_ import Token

class Scanner:
    def __init__(self, src: str):
        self.src = src
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan_token(self):
        c = self.advance()
        match c:
            case '(':
                self.add_token(TokenType.LEFT_PAREN)
            case ')':
                self.add_token(TokenType.RIGHT_PAREN)
            case '{':
                self.add_token(TokenType.LEFT_BRACE)
            case '}':
                self.add_token(TokenType.RIGHT_BRACE)
            case ',':
                self.add_token(TokenType.COMMA)
            case '.':
                self.add_token(TokenType.DOT)
            case '-':
                self.add_token(TokenType.MINUS)
            case '+':
                self.add_token(TokenType.PLUS)
            case ';':
                self.add_token(TokenType.SEMICOLON)
            case '*':
                self.add_token(TokenType.STAR)
            case _:
                from lox import error
                error(self.line, "Unexpected character.")

    def is_at_end(self):
        return self.current >= len(self.src)

    def advance(self):
        c = self.src[self.current]
        self.current += 1
        return c

    def add_token(self, type: TokenType):
        self.add_token(type, None)

    def add_token(self, type: TokenType, literal):
        text = self.src[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))