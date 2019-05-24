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
import getopt

def root():
    if not hasattr(root, "childs"):
        root.childs = {}


def dump_tree(root=root, lvl=0) -> str:
    tree_str = ""
    for top in root.childs:
        tree_str += "  "*lvl + str(top) + "\n" + dump_tree(root.childs[top], lvl + 1)
    return tree_str

def __expand_flags(cmd, opt):
    short_opts = ""
    long_opts = []
    for arg in cmd.arguments:
        short_opts += cmd.arguments[arg]["opt"][0]
        long_opts.append(arg)

    opts, args = getopt.getopt([opt], short_opts, long_opts)
    for o, a in opts:
        for arg in cmd.arguments:
            # Pretty ugly way to compare the actual flags, remove the
            # addition of the -
            if "-"+cmd.arguments[arg]["opt"] == o or "--" + arg == o:
                return arg + "=True"

def __exec_subcmd(cmd_list, cmds):
    word = cmds[0] 
    try:
        cmd = cmd_list[cmds[0]]
        # Last command in list or  leaf command
        if len(cmds) == 1 or len(cmd.childs) == 0:
            for idx, opt in enumerate(cmds):
                # Check if this is a flag or not
                if opt.startswith(('-', '--')):
                    exp = __expand_flags(cmd, opt)
                    cmds[idx] = exp
            try: 
                return cmd(*cmds[1:])
            except TypeError:
                raise ParserException("too many arguments")
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