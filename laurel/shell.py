from lexer import Lexer
from parser import Parser
from interpreter import Interpreter, Context

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
    result = interpreter.visit(ast.node, context)

    return result.value, result.error

print("Laurel Version 0.1.0 (Sprout)")
while True: 
    text = input('>>> ')

    if text in ["exit", "quit"]: break
    result, error = run('<shell>',text)

    if error: print(error.as_string())
    else: print(result)
