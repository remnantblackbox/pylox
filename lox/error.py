import sys
from token_ import Token
from token_type import TokenType
from runtime_error import LoxRuntimeError

had_error = False
had_runtime_error = False

def error(line: int, message: str):
    report(line, "", message)

def report(line: int, where: str, message: str):
    global had_error
    print(f"[line {line}] Error{where}: {message}", file=sys.stderr)
    had_error = True

def parse_error(token: Token, message:str):
    if token.type == TokenType.EOF:
        report(token.line, "at end", message)
    else:
        report(token.line, f" at '{token.lexeme}'", message)

def runtime_error(error: LoxRuntimeError):
    global had_runtime_error
    print(error.message + f"\n[line {error.token.line}]")
    had_runtime_error = True