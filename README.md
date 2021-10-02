# logidiff

A website and Python library for determining if two logical statements are equivalent. Uses VHDL syntax and logical operators.

| VHDL operator | Python operator | Left func | Right func|
|-|-|-|-|
| `not ` | `**` | `__pow__    ` | `            ` |
| `and ` | `/ ` | `__truediv__` | `__rtruediv__` |
| `or  ` | `+ ` | `__add__    ` | `__radd__    ` |
| `nand` | `<<` | `__lshift__ ` | `__rshift__  ` |
| `nor ` | `& ` | `__and__    ` | `__rand__    ` |
| `xor ` | `^ ` | `__xor__    ` | `__rxor__    ` |
| `xnor` | `\|` | `__or__     ` | `__ror__     ` |