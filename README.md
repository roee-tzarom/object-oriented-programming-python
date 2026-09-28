# Python OOP and Symbolic Expression Exercises

A small Python learning collection whose main component is an object-oriented symbolic expression engine in `symbolic_expression_engine.py`.

## Expression engine

An abstract `Expression` interface defines evaluation, variable discovery, substitution, differentiation and simplification. Concrete nodes represent numbers, variables, unary operations (`Neg`, `Sin`, `Cos`) and binary operations (`Add`, `Sub`, `Mul`, `Div`, `Pow`, `Log`). Operator overloads let expressions be assembled with ordinary Python arithmetic syntax.

```python
from symbolic_expression_engine import Num, Var, Sin

x = Var("x")
expr = Num(2) * x + Sin(x)
print(expr.evaluate({"x": 1.0}))
print(expr.differentiate("x").simplify())
```

The engine illustrates expression trees and transformation rules; it is not a complete computer algebra system. Some rules and simplifications are intentionally limited to the forms implemented in the source.

## Other exercises

| File | Focus |
| --- | --- |
| `data_types_exercises.py` | Lists, sets, dictionaries and sample log parsing |
| `text_recursion_exercises.py` | String processing and recursive digit operations |

Run `python symbolic_expression_engine.py` for its built-in demonstration, or run either other file separately. No third-party packages are required.
