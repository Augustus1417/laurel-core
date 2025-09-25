import lexer

print("Laurel Version 0.1.0 (Sprout)")
while True: 
    text = input('>>> ')

    if text in ["exit", "quit"]: break
    result, error = lexer.run('<shell>',text)

    if error: print(error.as_string())
    else: print(result)
