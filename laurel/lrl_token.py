from enum import Enum

class Type(Enum):
    INT = 'INT'
    FLOAT = 'FLOAT'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    MUL = 'MUL'
    DIV = 'DIV'
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    EOF = 'EOF'


class Token:
    def __init__(self, type_: Type, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
        else:
            self.pos_start = None

        if pos_end:
            self.pos_end = pos_end.copy()
        elif pos_start:
            # Default: token spans a single character
            self.pos_end = pos_start.copy()
            self.pos_end.advance(None)
        else:
            self.pos_end = None

    def __repr__(self):
        if self.value is not None:
            return f'{self.type}:{self.value}'
        return f'{self.type}'
