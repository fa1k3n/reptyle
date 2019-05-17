_commands = {}

def exec(cmd, args):
    _commands[cmd](*args)

def commands(parent = None):
    return _commands.keys()