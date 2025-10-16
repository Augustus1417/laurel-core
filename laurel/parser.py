from lrl_token import *
from errors import *
from position import *
from parser import *
from nodes import *

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error: self.error = res.error
            return res.node

        return res

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self
class Parser:
    def __init__(self,tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.current_tok = None
        self.advance()
    
    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def parse(self):
        res = self.expr()
        if not res.error and self.current_tok.type != Type.EOF:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '+', '-', '*', or '/'"
            ))
        return res
    
    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (Type.PLUS, Type.MINUS):
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))

        elif tok.type in (Type.INT, Type.FLOAT):
            res.register(self.advance())
            return res.success(NumberNode(tok))

        elif tok.type == Type.LPAREN:
            res.register(self.advance())
            expr = res.register(self.expr())
            if res.error: return res
            if self.current_tok.type == Type.RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ')'"
                ))
        
        return res.failure(InvalidSyntaxError(
            tok.pos_start, tok.pos_end, "Expected int or float"
        ))

    def term(self):
        return self.bin_op(self.factor, (Type.MUL, Type.DIV))

    def expr(self):
        return self.bin_op(self.term, (Type.PLUS, Type.MINUS))

    def bin_op(self, func, ops):
        res = ParseResult()
        left = res.register(func())
        if res.error: return res

        while self.current_tok.type in ops:
            op_tok = self.current_tok
            res.register(self.advance())
            right = res.register(func())
            if res.error: return res
            left = BinOpNode(left, op_tok, right)
        
        return res.success(left)