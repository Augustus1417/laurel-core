from runtime import *
from number import *
from lrl_token import *

class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos

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
        
        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))
    
    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        number = self.visit(node.node, context)
        if res.error: return res

        error = None

        if node.op_tok.type == Type.MINUS:
            number, error = number.multed_by(Number(-1))

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))