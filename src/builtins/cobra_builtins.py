from ..interpreter.interpreter import PythonFunction, Number, String, List, Boolean, Null
from .iostream import cb_print, cb_input


def populate_builtins(symbol_table):
    builtins = {
        "null": Null(),
        "print": PythonFunction("print", cb_print, ["value"]),
        "input": PythonFunction("input", cb_input, ["prompt"])
    }
    symbol_table.symbols.update(builtins)
