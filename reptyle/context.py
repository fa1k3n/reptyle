from reptyle.exception import ParserException

_commands = {}

def __exec_subcmd(cmd_list, cmds):
    try:
        cmd = cmd_list[cmds[0]]
        if len(cmd.childs) == 0:
            return cmd()
        else:
            return __exec_subcmd(cmd.childs, cmds[1:])
    except KeyError:
        raise ParserException("unknown command " + cmds[0])

def exec(cmds):
    cmds = cmds.split(" ")
    return __exec_subcmd(_commands, cmds)


def commands(parent = None):
    return _commands.keys()