from reptyle.console import Console, running
import reptyle.context as context
from functools import partial

def command(parent=None):
    if not isinstance(parent, partial):
        # Top level command
        fun = parent
        fun.childs = {}
        context._commands[fun.__name__] = fun

    def decorator(fun, parent=None):
        fun.childs = {}
        context._commands[parent.keywords["parent"].__name__].childs[fun.__name__] = fun
        return fun
    return partial(decorator, parent=parent)
