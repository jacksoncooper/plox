from typing import Any, Union

from plox.expressions import (
    Binary,
    Expr,
    Grouping,
    Literal,
    Unary,
    Visitor
)

import plox.token as token
from plox.token import TokenType as TT

Value = Union[token.Literal]

class Interpreter(Visitor):
    def visit_binary(self, expr: Binary) -> Any:
        pass
    
    def visit_grouping(self, expr: Grouping) -> Any:
        return self.evaluate(expr.expr)

    def visit_literal(self, expr: Literal) -> Value:
        return expr.value
    
    def visit_unary(self, expr: Unary) -> Any:
        right = self.evaluate(expr.right)
        
        type = expr.operator.type
        
        if type == TT.MINUS:
            return -right
        elif type == TT.BANG:
            return not self.is_truthy(right)
    
    def evaluate(self, expr: Expr) -> Any:
        return expr.accept(self)
    
    def is_truthy(self, value: Value) -> bool:
        if value is None: return False
        if isinstance(value, bool): return value
        return True
