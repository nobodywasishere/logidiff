# logidiff

A [website](https://blog.eowyn.net/logidiff/), Python 
library, and command line application for determining if two 
logical statements are equivalent. Uses VHDL syntax and logical 
operators. Also supports aliases for common operators, such as 
`*` for `and`, `+` for `or`, `!` for `not`, and `^` for xor.

Simply give it a logical equation and it will check every
input combination to find those that return false.
Multiple statements can be equated on the same line to check
their total equivalency.

## Examples

logidiff supports all of these equations, and correctly reports
each as being independently equivalent:

- `(a or b) and c = a*c+b*c`
- `(a xor b) and c = (a and c) xor (b and c)`
- `a xor b = a^b = !(a xnor b) = !a^!b`
- `a or b = !a nand !b = not (!a and !b)`

## CLI Usage

Call logidiff and pass the equation to evaluate via stdin.
It may need to be wrapped in single quotes depending on your shell.
The failed cases will be printed to stdout.

```bash
$ logidiff '(a and b) or c = a'

Statements not equivalent for inputs:
  a: 0, b: 0, c: 1
  a: 0, b: 1, c: 1
  a: 1, b: 0, c: 0

$ ./logidiff.py 'a*(b+c)=a*b+a*c'

Statements are equivalent

$ ./logidiff.py 'a^b=!a xor !b'

Statements are equivalent
```

## Library Usage

```python

# Import the logidiff evaluate function
from logidiff import evaluate

# This is the string to evaluate
test = "(a or b) and c = (a and c) or (b and c)"

# Returns the cases that aren't true
#   as a list of strings
cases = evaluate(test)

# Print the cases
for ne in cases:
    print(', '.join(ne))

```

## Website Usage

The website utilizes [Brython](http://brython.info/) as a 
Python interpreter and requires no server-side code to operate.
Simply type in the logical equation to evaluate and press enter.

## Special thanks

Special thanks to [zpogrebin](https://github.com/zpogrebin) for
his help in fleshing out the initial idea and implementation
of this project.

---

## How does it work?

logidiff works by finding all of the non-reserved words within
the statement and assumes they are the variables to be tested.
It then goes through and replaces all of the reserved words
(the logical operations `and`, `or`, `xor`, etc) with Python infix
operators that implement those functions. This is because 
Python does not have all the logical statements that VHDL has,
and the operator precedence is slightly different. Finally,
logidiff simply evaluates the resulting equation as Python code,
setting each of the variables to a value, and checking to see
if the result is true or false. It does this for every possible
combination of input values.

## Internal Infix Operators

Infix operators have been around for a long time in Python,
but have never really taken off. More information about
what they are and how they work can be found 
[here](https://code.activestate.com/recipes/384122-infix-operators/). 
This table describes the VHDL operator and which
Python operators they are switched with internally.
As `not` only needs to operate on the right side, it does 
not have a left infix operator.

| VHDL operator | Alias | Python infix operator | Left func | Right func|
|--------|-----|------|---------------|----------------|
| `not ` | `!` | `**` |               | `__pow__     ` |
| `and ` | `*` | `/ ` | `__truediv__` | `__rtruediv__` |
| `or  ` | `+` | `+ ` | `__add__    ` | `__radd__    ` |
| `nand` |     | `<<` | `__lshift__ ` | `__rshift__  ` |
| `nor ` |     | `& ` | `__and__    ` | `__rand__    ` |
| `xor ` | `^` | `^ ` | `__xor__    ` | `__rxor__    ` |
| `xnor` |     | `\|` | `__or__     ` | `__ror__     ` |