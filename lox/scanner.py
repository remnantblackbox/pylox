from token_type import TokenType
from token_ import Token
import error

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
            case '!':
                self.add_token(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
            case '=':
                self.add_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
            case '<':
                self.add_token(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
            case '>':
                self.add_token(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)
            case '/':
                if self.match('/'):
                    while self.peek() != '\n' and not self.is_at_end():
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)
            case ' ' | '\r' | '\t':
                pass
            case '\n':
                self.line += 1
            case '"':
                self.string()
            case _:
                if self.is_digit(c):
                    self.number()
                else:
                    error.error(self.line, "Unexpected character.")

    def number(self):
        while self.is_digit(self.peek()):
            self.advance()

        # Look for a fractional part
        if self.peek() == '.' and self.is_digit(self.peek_next()):
            # Consume the "."
            self.advance()
            while self.is_digit(self.peek()):
                self.advance()

        self.add_token(TokenType.NUMBER, float(self.src[self.start:self.current]))

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if self.is_at_end():
            error.error(self.line, "Unterminated string.")
            return

        # The closing ".
        self.advance()

        # Trim the surrounding quotes.
        value = self.src[self.start+1:self.current-1]
        self.add_token(TokenType.STRING, value)

    def match(self, expected: str):
        if self.is_at_end(): 
            return False
        if self.src[self.current] != expected: 
            return False

        self.current += 1
        return True

    def peek(self):
        if self.is_at_end(): 
            return '\0'
        return self.src[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.src): 
            return '\0'
        return self.src[self.current+1]

    def is_digit(self, c):
        return '0' <= c <= '9'

    def is_at_end(self):
        return self.current >= len(self.src)

    def advance(self):
        c = self.src[self.current]
        self.current += 1
        return c

    def add_token(self, type: TokenType, literal=None):
        text = self.src[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))