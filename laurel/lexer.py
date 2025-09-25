from lrl_token import *
from constants import *
from errors import *
from position import *

class Lexer:
    def __init__(self, filename, text):
        self.filename = filename
        self.text = text
        self.pos = Position(-1, 0, -1, filename, text)
        self.current_char = None
        self.advance()
    
    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.index] if self.pos.index < len(self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in Constants.DIGITS:
                tokens.append(self.make_number())
                self.advance()
            elif self.current_char == '+':
                tokens.append(Token(Type.PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(Type.MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(Type.MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(Type.DIV))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(Type.LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(Type.RPAREN))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, f"'{char}'")
        
        return tokens, None
                
    def make_number(self):
        num_str = ''
        dot_count = 0

        while self.current_char != None and self.current_char in Constants.DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1:break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()
            
        if dot_count == 0:
            return Token(Type.INT, int(num_str))
        else:
            return Token(Type.FLOAT, float(num_str))
    
def run(filename, text):
    lexer = Lexer(filename, text)
    tokens, error = lexer.make_tokens()

    return tokens, error
