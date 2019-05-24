# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from reptyle.console import Console, running
import reptyle.context as context
from reptyle.exception import GeneralException
import inspect
from collections import OrderedDict

def __add_cmd(parent, name, fun):
    if not hasattr(fun, "childs"):
        fun.childs = {}
    if name in parent.childs:
        raise GeneralException(f"command {name} is already a registered command")
    parent.childs[name] = fun


def command(_func = None, *, parent = context.root, name = None):
    context.root()

    def wrapper(func, parent = parent, name = name):
        if name is None:
            name = func.__name__
        func_spec = inspect.getfullargspec(func)

        if not hasattr(func, "arguments") and len(func_spec.args) > 0:
            # Command function seem to have arguments, but none is defined
            raise exception.GeneralException(f"numbers of arguments does not match")
        __add_cmd(parent, name, func)
        return func

    if _func is None:
        return wrapper
    else:
        return wrapper(_func, parent, name)

def argument(name, description=None, flags=None):
    def wrapper(func):
        func_spec = inspect.getfullargspec(func)
        args = func_spec.args
        if name not in args:
            raise exception.GeneralException(f"argument {name} does not exist in function {func.__name__}")
        if not hasattr(func, "arguments"):
            func.arguments = OrderedDict()
        func.arguments[name] = {}
        func.arguments[name]["description"] = description
        func.arguments[name]["flags"] = flags
        return func
    return wrapper