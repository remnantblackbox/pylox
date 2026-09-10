import sys
from scanner import Scanner
from parser import Parser
from ast_printer import AstPrinter
import error

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
    expression = parser.parse()

    if error.had_error:
        return

    print(AstPrinter().print(expression))

if __name__ == "__main__":
    main()