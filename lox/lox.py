import sys
from scanner import Scanner
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
    scanner = Scanner(src) # still to be defined
    tokens = scanner.scan_tokens()

    for token in tokens:
        print(token)



if __name__ == "__main__":
    main()