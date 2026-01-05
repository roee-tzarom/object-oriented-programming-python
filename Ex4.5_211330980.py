import math
from abc import ABC, abstractmethod


def ensure_expr(value):
    if isinstance(value, Expression):
        return value
    if isinstance(value, (int, float)):
        return Num(float(value))
    raise ValueError("Invalid operand type")


class Expression(ABC):
    @abstractmethod
    def evaluate(self, env):
        pass

    @abstractmethod
    def variables(self):
        pass

    @abstractmethod
    def assign(self, var, expr):
        pass

    @abstractmethod
    def differentiate(self, var):
        pass

    @abstractmethod
    def simplify(self):
        pass

    def __add__(self, other): return Add(self, ensure_expr(other))

    def __radd__(self, other): return Add(ensure_expr(other), self)

    def __sub__(self, other): return Sub(self, ensure_expr(other))

    def __rsub__(self, other): return Sub(ensure_expr(other), self)

    def __mul__(self, other): return Mul(self, ensure_expr(other))

    def __rmul__(self, other): return Mul(ensure_expr(other), self)

    def __truediv__(self, other): return Div(self, ensure_expr(other))

    def __rtruediv__(self, other): return Div(ensure_expr(other), self)

    def __pow__(self, other): return Pow(self, ensure_expr(other))

    def __rpow__(self, other): return Pow(ensure_expr(other), self)

    def __neg__(self): return Neg(self)

    @abstractmethod
    def __str__(self):
        pass


class UnaryOp(Expression):
    def __init__(self, expr):
        self.expr = ensure_expr(expr)

    def variables(self):
        return self.expr.variables()

    def assign(self, var, repl):
        return self.__class__(self.expr.assign(var, repl))


class BinaryOp(Expression):
    def __init__(self, left, right):
        self.left = ensure_expr(left)
        self.right = ensure_expr(right)

    def variables(self):
        return self.left.variables() | self.right.variables()

    def assign(self, var, repl):
        return self.__class__(self.left.assign(var, repl), self.right.assign(var, repl))


class Num(Expression):
    def __init__(self, value):
        self.value = float(value)

    def evaluate(self, env):
        return self.value

    def variables(self):
        return set()

    def assign(self, var, expr):
        return self

    def differentiate(self, var):
        return Num(0.0)

    def simplify(self):
        return self

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return isinstance(other, Num) and self.value == other.value


class Var(Expression):
    def __init__(self, name):
        self.name = name

    def evaluate(self, env):
        if self.name not in env:
            raise ValueError(f"Variable {self.name} not in environment")
        return env[self.name]

    def variables(self):
        return {self.name}

    def assign(self, var, expr):
        if self.name == var:
            return expr
        return self

    def differentiate(self, var):
        if self.name == var:
            return Num(1.0)
        return Num(0.0)

    def simplify(self):
        return self

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return isinstance(other, Var) and self.name == other.name


class Neg(UnaryOp):
    def evaluate(self, env):
        return -self.expr.evaluate(env)

    def differentiate(self, var):
        return Neg(self.expr.differentiate(var))

    def simplify(self):
        simple_expr = self.expr.simplify()
        if isinstance(simple_expr, Num):
            return Num(-simple_expr.value)
        return Neg(simple_expr)

    def __str__(self):
        return f"(-{self.expr})"


class Sin(UnaryOp):
    def evaluate(self, env):
        return math.sin(self.expr.evaluate(env))

    def differentiate(self, var):
        return Mul(Cos(self.expr), self.expr.differentiate(var))

    def simplify(self):
        simple_expr = self.expr.simplify()
        if isinstance(simple_expr, Num):
            return Num(math.sin(simple_expr.value))
        return Sin(simple_expr)

    def __str__(self):
        return f"sin({self.expr})"


class Cos(UnaryOp):
    def evaluate(self, env):
        return math.cos(self.expr.evaluate(env))

    def differentiate(self, var):
        return Mul(Neg(Sin(self.expr)), self.expr.differentiate(var))

    def simplify(self):
        simple_expr = self.expr.simplify()
        if isinstance(simple_expr, Num):
            return Num(math.cos(simple_expr.value))
        return Cos(simple_expr)

    def __str__(self):
        return f"cos({self.expr})"


class Add(BinaryOp):
    def evaluate(self, env):
        return self.left.evaluate(env) + self.right.evaluate(env)

    def differentiate(self, var):
        return Add(self.left.differentiate(var), self.right.differentiate(var))

    def simplify(self):
        l = self.left.simplify()
        r = self.right.simplify()
        if isinstance(l, Num) and isinstance(r, Num):
            return Num(l.value + r.value)
        if isinstance(l, Num) and l.value == 0: return r
        if isinstance(r, Num) and r.value == 0: return l
        return Add(l, r)

    def __str__(self):
        return f"({self.left} + {self.right})"


class Sub(BinaryOp):
    def evaluate(self, env):
        return self.left.evaluate(env) - self.right.evaluate(env)

    def differentiate(self, var):
        return Sub(self.left.differentiate(var), self.right.differentiate(var))

    def simplify(self):
        l = self.left.simplify()
        r = self.right.simplify()
        if isinstance(l, Num) and isinstance(r, Num):
            return Num(l.value - r.value)
        if isinstance(r, Num) and r.value == 0: return l
        if str(l) == str(r): return Num(0.0)
        return Sub(l, r)

    def __str__(self):
        return f"({self.left} - {self.right})"


class Mul(BinaryOp):
    def evaluate(self, env):
        return self.left.evaluate(env) * self.right.evaluate(env)

    def differentiate(self, var):
        return Add(Mul(self.left.differentiate(var), self.right),
                   Mul(self.left, self.right.differentiate(var)))

    def simplify(self):
        l = self.left.simplify()
        r = self.right.simplify()
        if isinstance(l, Num) and isinstance(r, Num):
            return Num(l.value * r.value)
        if isinstance(l, Num):
            if l.value == 0: return Num(0.0)
            if l.value == 1: return r
        if isinstance(r, Num):
            if r.value == 0: return Num(0.0)
            if r.value == 1: return l
        return Mul(l, r)

    def __str__(self):
        return f"({self.left} * {self.right})"


class Div(BinaryOp):
    def evaluate(self, env):
        return self.left.evaluate(env) / self.right.evaluate(env)

    def differentiate(self, var):
        numerator = Sub(Mul(self.left.differentiate(var), self.right),
                        Mul(self.left, self.right.differentiate(var)))
        denominator = Pow(self.right, Num(2))
        return Div(numerator, denominator)

    def simplify(self):
        l = self.left.simplify()
        r = self.right.simplify()

        # חישוב נומרי רגיל
        if isinstance(l, Num) and isinstance(r, Num):
            return Num(l.value / r.value)

        # --- הוספנו את זה: 0 חלקי כל דבר שווה 0 ---
        if isinstance(l, Num) and l.value == 0:
            return Num(0.0)
        # ----------------------------------------

        if str(l) == str(r): return Num(1.0)  # X / X = 1
        return Div(l, r)

    def __str__(self):
        return f"({self.left} / {self.right})"


class Pow(BinaryOp):
    def evaluate(self, env):
        return self.left.evaluate(env) ** self.right.evaluate(env)

    def differentiate(self, var):
        base = self.left
        exp = self.right
        term1 = Mul(exp.differentiate(var), Log(Var("e"), base))
        term2 = Mul(exp, Div(base.differentiate(var), base))
        return Mul(Pow(base, exp), Add(term1, term2))

    def simplify(self):
        l = self.left.simplify()
        r = self.right.simplify()
        if isinstance(l, Num) and isinstance(r, Num):
            return Num(l.value ** r.value)
        if isinstance(r, Num) and r.value == 0: return Num(1.0)
        if isinstance(r, Num) and r.value == 1: return l
        return Pow(l, r)

    def __str__(self):
        return f"({self.left}^{self.right})"


class Log(BinaryOp):
    def evaluate(self, env):
        return math.log(self.right.evaluate(env), self.left.evaluate(env))

    def differentiate(self, var):
        return Div(self.right.differentiate(var),
                   Mul(self.right, Log(Var("e"), self.left)))

    def simplify(self):
        l = self.left.simplify()
        r = self.right.simplify()
        if isinstance(l, Num) and isinstance(r, Num):
            return Num(math.log(r.value, l.value))
        if str(l) == str(r): return Num(1.0)
        return Log(l, r)

    def __str__(self):
        return f"log({self.left}, {self.right})"


if __name__ == "__main__":
    print("=== בדיקת המנוע המתמטי ===")

    x = Var("x")
    y = Var("y")
    e = Var("e")

    expr = (Num(2) * x) + Sin(Num(4) * y) + (e ** x)

    print("\n1. הביטוי המקורי:")
    print(expr)

    env = {"x": 2.0, "y": 0.25, "e": 2.71}
    result = expr.evaluate(env)
    print("\n2. תוצאת החישוב (עבור x=2, y=0.25):")
    print(result)

    deriv = expr.differentiate("x")
    print("\n3. הנגזרת לפני פישוט (Unsimplified):")
    print(deriv)

    simplified = deriv.simplify()
    print("\n4. הנגזרת אחרי פישוט (simplify):")
    print(simplified)