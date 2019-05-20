from reptyle.exception import ParserException



def root():
    if not hasattr(root, "childs"):
        root.childs = {}

def __exec_subcmd(cmd_list, cmds):
    try:
        cmd = cmd_list[cmds[0]]
        # Last command in list or leaf command
        if len(cmds) == 1 or len(cmd.childs) == 0:
            return cmd()
        else:
            return __exec_subcmd(cmd.childs, cmds[1:])
    except KeyError:
        raise ParserException("unknown command " + cmds[0])

def exec(cmds):
    cmds = cmds.split(" ")
    return __exec_subcmd(root.childs, cmds)

def commands(parent = root):
    return parent.childs.keys()