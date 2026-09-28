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


## Inside the expression tree

An expression is represented as a node rather than an immediately computed value. `Var` and `Num` are leaves; arithmetic and trigonometric classes combine them into larger trees. Evaluating a tree walks its nodes with a variable environment. Differentiating it creates another tree according to the rule implemented by each node. Simplification then removes supported redundant forms. The overloaded arithmetic operators make construction concise while the underlying objects remain inspectable.

For example, build an expression with `Var("x")`, substitute a value for `x`, evaluate it, then request a derivative and simplify the resulting tree. This separation between representation and transformation is the main design idea. The `__main__` demonstration in `symbolic_expression_engine.py` provides further runnable examples.

## Repository map

`data_types_exercises.py` practices common container operations and a sample log-line parse. `text_recursion_exercises.py` explores text routines and recursive digit work. Neither script depends on the expression engine, so each can be run independently with Python 3.

## Limits

The differentiation and simplification code supports the node types and rewrite rules present in the file. It does not attempt arbitrary symbolic identities, equation solving or a general parser for user-entered expressions. Use it as a compact example of polymorphism and tree transformations rather than a replacement for a computer algebra package.
