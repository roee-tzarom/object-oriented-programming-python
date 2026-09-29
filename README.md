# Python Expression Trees and Data Utilities

A Python collection centered on a symbolic mathematics engine. It models an expression as a tree of objects, then walks or transforms that tree to evaluate values, substitute variables, differentiate and simplify supported forms. Two smaller scripts explore text, recursion and Python collections.

## Symbolic expression engine

`symbolic_expression_engine.py` defines an abstract `Expression` interface. `Num` and `Var` are leaves; unary and binary nodes combine them into formulas. Supported operations include addition, subtraction, multiplication, division, powers, logarithms, negation, sine and cosine. Operator overloads allow normal Python arithmetic syntax while preserving the expression tree.

```python
from symbolic_expression_engine import Num, Sin, Var

x = Var("x")
expression = Num(2) * x + Sin(x)
print(expression.evaluate({"x": 1.0}))
print(expression.differentiate("x").simplify())
```

Evaluation uses a variable environment. Differentiation creates a new tree according to each node's rule, and simplification applies the rewrite rules implemented by the engine. The source also supports variable discovery and substitution. This is an inspectable model of symbolic transformations rather than a parser for arbitrary user-entered formulas.

## Other Python components

| File | Focus |
| --- | --- |
| `data_types_exercises.py` | Aggregate calculations, set operations, dictionary filtering and sample log fields |
| `text_recursion_exercises.py` | String processing, text framing and recursive digit functions |

Each file can run independently with Python 3 and the standard library:

```bash
python symbolic_expression_engine.py
python data_types_exercises.py
python text_recursion_exercises.py
```

## Suggested reading path

Start with `Expression`, `Num` and `Var`; then inspect the unary and binary base classes to see which behavior is shared. Follow `differentiate` on the concrete operations and compare the resulting tree with `simplify`. The other two scripts are separate, short demonstrations of core language features.

The symbolic rules cover the node types present in the source. The project does not provide equation solving, a full algebra system or an input-language parser.
