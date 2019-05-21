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

from reptyle.exception import ParserException


def root():
    if not hasattr(root, "childs"):
        root.childs = {}


def dump_tree(root=root, lvl=0) -> str:
    tree_str = ""
    for top in root.childs:
        tree_str += "  "*lvl + str(top) + "\n" + dump_tree(root.childs[top], lvl + 1)
    return tree_str


def __exec_subcmd(cmd_list, cmds):
    try:
        cmd = cmd_list[cmds[0]]
        # Last command in list or leaf command
        if len(cmds) == 1 or len(cmd.childs) == 0:
            return cmd(*cmds[1:])
        else:
            return __exec_subcmd(cmd.childs, cmds[1:])
    except KeyError:
        raise ParserException("unknown command " + cmds[0])


def exec(cmds):
    cmds = cmds.split(" ")
    try:
        return __exec_subcmd(root.childs, cmds)
    except AttributeError:
        raise ParserException("unknown command " + cmds[0])


def commands(parent = root):
    return parent.childs.keys()