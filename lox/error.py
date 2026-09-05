import sys

had_error = False

def error(line: int, message: str):
    report(line, "", message)

def report(line: int, where: str, message: str):
    global had_error
    print(f"[line {line}] Error{where}: {message}", file=sys.stderr)
    had_error = True