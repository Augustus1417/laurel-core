import lexer

while True: 
    text = input('lrl > ')
    result, error = lexer.run('<shell>',text)

    if error: print(error.as_string())
    else: print(result)