from lexer import Lexer
from parser import Parser
from interpreter import Interpreter, Context, SymbolTable, Number

global_symbol_table = SymbolTable()
global_symbol_table.set("NULL", Number(0))
global_symbol_table.set("TRUE", Number(1))
global_symbol_table.set("FALSE", Number(0))
 
def run(filename, text):
    lexer = Lexer(filename, text)
    tokens, error = lexer.make_tokens()
    if error: return None, error

    parser = Parser(tokens)
    # generate AST
    ast = parser.parse()
    if ast.error: return None, ast.error

    # run program
    interpreter = Interpreter()
    context = Context('<program>')
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error

print("Laurel Version 0.1.0 (Sprout)")
while True: 
    text = input('>>> ')

    if text in ["exit", "quit"]: break
    result, error = run('<shell>',text)

    if error: print(error.as_string())
    elif result: print(result)
