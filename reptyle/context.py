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

def __generate_short_arg_str(args):
    short_opts = ""
    for arg in args:
        short_opts += str(args[arg]["opt"])
        if args[arg]["type"] is not bool:
            short_opts += ":"
    return short_opts

def __get_long_option(func, o):
    if o.startswith("--"):
        # Already long name, just retun value
        return o[2:]
    # Skip - infront of flag
    o = o[1:]
    for arg in func.arguments:
        if func.arguments[arg]["opt"] == o:
            return arg
    return None


def __expand_flags(cmd_list, cmds):
    func = cmd_list[cmds[0]]
    ret_pos_args = []

    if not hasattr(func, "arguments"):
        # Not any arguments, just return
        return (cmds[1:], {})

    fun_args = func.arguments

    short_opts = __generate_short_arg_str(fun_args)
    try:
        opts, args = getopt.getopt(cmds[1:], short_opts, fun_args.keys())
    except getopt.GetoptError as e:
        raise ParserException(e) 
    ret_named_args = {}

    idx = 1
    while idx < len(cmds):
        cmd = cmds[idx]
        arg_found = False
        for o, a in opts:
            if cmd in o:
                arg_found = True
                if a is not "":
                    # This is an assigment, skip value as that 
                    # is part of the getopt structure
                    idx += 1
                else:
                    # This is a flag, set to True
                    a = True
                long_opt = __get_long_option(func, o)
                ret_named_args[long_opt] = fun_args[long_opt]["type"](a)
        if not arg_found:
            ret_pos_args.append(cmd)
        idx += 1
    return (ret_pos_args, ret_named_args)

def __exec_subcmd(cmd_list, cmds):
    word = cmds[0] 
    try:
        cmd = cmd_list[cmds[0]]
        # Last command in list or  leaf command
        if len(cmds) == 1 or len(cmd.childs) == 0:
            pos, named = __expand_flags(cmd_list, cmds)
            try: 
                return cmd(*pos, **named)
                #return cmd(*cmds[1:])
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