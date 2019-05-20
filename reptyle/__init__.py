from reptyle.console import Console, running
import reptyle.context as context
from functools import partial

def __add_cmd(parent, name, fun):
    if not hasattr(fun, "childs"):
        fun.childs = {}
    parent.childs[name] = fun

def command(parent=None):
    if not isinstance(parent, partial):
        # Top level command
        context.root()
        __add_cmd(context.root, parent.__name__, parent)

    def decorator(fun, parent=None):
        __add_cmd(parent.keywords["parent"], fun.__name__, fun)
        return fun
    return partial(decorator, parent=parent)
