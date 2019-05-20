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


def __add_cmd(parent, name, fun):
    if not hasattr(fun, "childs"):
        fun.childs = {}
    parent.childs[name] = fun


def command(_func = None, *, parent = context.root):
    def wrapper(func, parent = parent):
        __add_cmd(parent, func.__name__, func)
        return func

    if _func is None:
        return wrapper
    else:
        # Top level cmd, init root element if needed
        context.root()
        return wrapper(_func, parent)