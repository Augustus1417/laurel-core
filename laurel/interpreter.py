from runtime import RTResult
from errors import RTError
from number import Number
from lrl_token import Type

class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None

class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.parent = None
    
    def get(self, name):
        value = self.symbols.get(name, None)
        if value == None and self.parent:
            return self.parent.get(name)
        return value
    
    def set(self, name, value):
        self.symbols[name] = value
    
    def remove(self, name):
        del self.symbols[name]


class Interpreter:
    def visit(self, node, context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self , node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')
    
    def visit_NumberNode(self, node, context):
        return RTResult().success(
            Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )
    
    def visit_VarAccessNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)

        if not value:
            return res.failure(RTError(
                node.pos_start, node.pos_end,
                f"{var_name} is not defined",
                context
            ))
        
        value = value.copy().set_pos(node.pos_start, node.pos_end)
        return res.success(value)
    
    def visit_VarAssignNode(self, node, context):
        res = RTResult()

        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.error: return res

        context.symbol_table.set(var_name, value)
        return res.success(value)

    
    def visit_BinOpNode(self, node, context):
        res = RTResult()
        left = res.register(self.visit(node.left_node, context))
        if res.error: return res
        right = res.register(self.visit(node.right_node, context))

        if node.op_tok.type == Type.PLUS:
            result, error = left.added_to(right)
        elif node.op_tok.type == Type.MINUS:
            result, error = left.subbed_by(right)
        elif node.op_tok.type == Type.MUL:
            result, error = left.multed_by(right)
        elif node.op_tok.type == Type.DIV:
            result, error = left.divided_by(right)
        elif node.op_tok.type == Type.POW:
            result, error = left.powed_by(right)
        elif node.op_tok.type == Type.EE:
            result, error = left.get_comparison_eq(right)
        elif node.op_tok.type == Type.NE: 
            result, error = left.get_comparison_ne(right) 
        elif node.op_tok.type == Type.LT: 
            result, error = left.get_comparison_lt(right) 
        elif node.op_tok.type == Type.GT: 
            result, error = left.get_comparison_gt(right) 
        elif node.op_tok.type == Type.LTE: 
            result, error = left.get_comparison_lte(right) 
        elif node.op_tok.type == Type.GTE: 
            result, error = left.get_comparison_gte(right) 
        elif node.op_tok.matches(Type.KEYWORD, 'AND'): 
            result, error = left.anded_by(right) 
        elif node.op_tok.matches(Type.KEYWORD, 'OR'): 
            result, error = left.ored_by(right)

        
        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))
    
    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        number = res.register(self.visit(node.node, context))
        if res.error: return res

        error = None

        if node.op_tok.type == Type.MINUS:
            number, error = number.multed_by(Number(-1))
        if node.op_tok.matches(Type.KEYWORD, 'NOT'):
            number, error = number.notted()

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))