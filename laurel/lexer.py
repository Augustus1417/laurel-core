from lrl_token import *
from errors import *
import string

class Constants:
    DIGITS = '0123456789'
    LETTERS = string.ascii_letters
    LETTERS_DIGITS = LETTERS + DIGITS

    KEYWORDS = [
        'VAR',
        'AND',
        'OR',
        'NOT',
        'IF',
        'THEN',
        'ELIF',
        'ELSE'
    ]

class Position:
    def __init__(self, index, ln, col, filename, filetxt):
        self.index = index
        self.ln = ln
        self.col = col
        self.filename = filename
        self.filetxt = filetxt
    
    def advance(self, current_char):
        self.index += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0
        return self
    
    def copy(self):
        return Position(self.index, self.ln, self.col, self.filename, self.filetxt)

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
            elif self.current_char in Constants.LETTERS:
                tokens.append(self.make_identifier())
            elif self.current_char == '+':
                tokens.append(Token(Type.PLUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(Type.MINUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(Type.MUL, pos_start=self.pos))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(Type.DIV, pos_start=self.pos))
                self.advance()
            elif self.current_char == '^':
                tokens.append(Token(Type.POW, pos_start=self.pos))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(Type.LPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(Type.RPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == '!':
                tok, error = self.make_not_equals()
                if error: return [], error
                tokens.append(tok)
            elif self.current_char == '=':
                tokens.append(self.make_equals())
            elif self.current_char == '<':
                tokens.append(self.make_less_than())
            elif self.current_char == '>':
                tokens.append(self.make_greater_than())
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, f"'{char}'")
        
        tokens.append(Token(Type.EOF, pos_start=self.pos))
        return tokens, None
                
    def make_number(self):
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in Constants.DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1:break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()
            
        if dot_count == 0:
            return Token(Type.INT, int(num_str), pos_start, self.pos)
        else:
            return Token(Type.FLOAT, float(num_str), pos_start, self.pos)
    
    def make_identifier(self):
        id_str = ''
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in Constants.LETTERS_DIGITS + '_':
            id_str += self.current_char
            self.advance()
        
        tok_type = Type.KEYWORD if id_str in Constants.KEYWORDS else Type.IDENTIFIER
        return Token(tok_type, id_str, pos_start, self.pos)
    
    def make_not_equals(self):
        pos_start = self.post.copy()
        self.advance()
        if self.current_char == '=':
            self.advance()
            return Token(Type.NE, pos_start=pos_start, pos_end=self.pos), None

        self.advance()
        return None, ExpectedCharError(pos_start, self.pos, "'=' (after '!')")

    def make_less_than(self):
        tok_type = Type.LT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = Type.LTE
        
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_greater_than(self):
        tok_type = Type.GT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = Type.GTE
        
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)
    def make_equals(self):
        tok_type = Type.EQ
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = Type.EE
        
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)
