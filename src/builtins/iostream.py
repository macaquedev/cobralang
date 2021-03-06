from ..interpreter.interpreter import RTResult, Number, String


def cb_print(symbol_table):
    print(str(symbol_table.get("value")))
    return symbol_table.get("null")


def cb_input(symbol_table):
    print(symbol_table.get("prompt"))
    return String(input(str(symbol_table.get("prompt"))))
