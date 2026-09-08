from token_ import Token
from token_type import TokenType
from expr import Expr, Binary

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0

    def expression(self):
        return self.equality()

    def equality(self):
        expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    def match(self, *types: TokenType):
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def check(self, token_type: TokenType):
        if self.is_at_end():
            return False
        return type(self.peek()) == token_type

    def advance(self):
        if self.is_at_end():
            current += 1
        return self.previous()

    def is_at_end(self):
        return type(self.peek()) == TokenType.EOF

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]