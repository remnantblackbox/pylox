# pylox

A tree-walking interpreter for the Lox programming language, written in Python.

## The Lox language

Lox is the language designed in the book [*Crafting Interpreters*](https://craftinginterpreters.com/) by Robert Nystrom. It's compact and high-level, in the same spirit as scripting languages like JavaScript or Lua: it's dynamically typed, has a C-like syntax, and supports variables, control flow, first-class functions, closures and classes with inheritance.

Here's what Lox looks like:
 
```
fun make_counter() {
  var count = 0;
  fun counter() {
    count = count + 1;
    return count;
  }
  return counter;
}
 
var counter = make_counter();
print counter(); // 1
print counter(); // 2
```

## Overview

In the first part of the book, Robert Nystrom builds **jlox**, an interpreter for Lox written in Java. **pylox** is my version of it with a few changes of my own.

I decided to port the interpreter to Python because I didn't want to just copy the Java code from the book line by line. Porting it forced me to actually understand what each piece does before writing it and gave me room to try things a bit differently where Python allowed it.

Being a tree-walking interpreter, pylox builds a syntax tree from the source code and then walks it, executing each node along the way.

When you run a script or type some code in the REPL, the scanner (`lox/scanner.py`) reads the code and splits it into tokens: keywords, identifiers, numbers, strings, operators and so on. The parser (`lox/parser.py`) takes those tokens and builds the syntax tree with recursive descent. The tree nodes are in `lox/expr.py` for expressions and `lox/stmt.py` for statements.

Before running anything, the resolver (`lox/resolver.py`) walks the tree once to figure out which declaration each variable refers to and how many scopes away it is. Thanks to this, the interpreter can go straight to the right scope when it looks up a variable, and closures always see the variables they captured. The resolver also catches a couple of errors early, like declaring the same variable twice in the same scope or using `return` outside a function.

Then the interpreter (`lox/interpreter.py`) walks the tree again and actually runs it, storing variables in the environments defined in `lox/environment.py`.

## Progress

The interpreter covers the book up to chapter 11:

* scanning, parsing and evaluating expressions
* statements, variables and block scope
* control flow (`if`, `while`, `for`, `and`, `or`)
* functions, a native `clock` function and closures
* the resolver pass for static variable resolution

Classes (chapter 12) and inheritance (chapter 13) are next.

## Differences from the book and design choices

For the most part pylox follows jlox closely, except for a few things:

* **No Visitor pattern.** The book uses the Visitor pattern to walk the syntax tree, which makes sense in Java. Python 3.10 has structural pattern matching, so the interpreter and the resolver just `match` on the node type instead. I started out with visitors, but in Python they just added boilerplate without really giving me anything back.
* **Environments passed as parameters.** In the book, the interpreter keeps the current environment in a field, and every block has to swap it with a new one and then restore the previous one at the end (inside a `try`/`finally`, so it gets restored even if an error is raised). In pylox I pass the environment as a parameter to `evaluate` and `execute` instead. A block creates a new environment and passes it down, and when the block ends there's nothing to restore, since the caller still has its own. The interpreter's field only holds the global environment.
* **Anonymous functions.** I added lambdas, so functions can also be written inline without a name:

```
var add = fun (a, b) { return a + b; };
print add(1, 2); // 3
```

## Running it

Requires Python 3.10+ (for `match`)

To start the REPL:
```
python lox/lox.py
```

To run a script:
```
python lox/lox.py path/to/script.lox
```

## Tests

The `tests/` folder contains Lox scripts taken from the book's official [test suite](https://github.com/munificent/craftinginterpreters/tree/master/test). Each script has `// expect:` comments with the expected output, or `// expect runtime error:` when the script is supposed to fail.

There's no test runner yet, so for now I run them by hand:
```
python lox/lox.py tests/closure/nested_closure.lox
```

## What's next

Finishing pylox with classes and inheritance, and porting the rest of the tests.

## Credits

Lox and jlox are by Robert Nystrom, from [*Crafting Interpreters*](https://craftinginterpreters.com/).
