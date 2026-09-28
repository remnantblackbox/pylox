import sys
from scanner import Scanner
from parser import Parser
from interpreter import Interpreter
from resolver import Resolver
from ast_printer import AstPrinter
import error

interpreter = Interpreter()

def main():
    args = sys.argv[1:]
    if len(args) > 1:
        print("Usage: pylox [script]")
        sys.exit(64)
    elif len(args) == 1:
        run_file(args[0])
    else:
        run_prompt()

def run_file(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        src = f.read()
    run(src)
    if error.had_error:
        sys.exit(65)
    if error.had_runtime_error:
        sys.exit(70)

def run_prompt():
    while True:
        try:
            line = input("> ")
        except EOFError:
            break
        run(line)
        error.had_error = False

def run(src: str):
    scanner = Scanner(src)
    tokens = scanner.scan_tokens()
    parser = Parser(tokens)
    statements = parser.parse()

    if error.had_error:
        return

    resolver = Resolver(interpreter)
    resolver.resolve(statements)
    interpreter.interpret(statements)

if __name__ == "__main__":
    main()