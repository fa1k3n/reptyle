import reptyle
from reptyle import command

@command
def foo():
    print("FOO")

@command(parent=foo)
def bar():
    print("BAR")

@command(parent=foo)
def baz():
    print("BAZ")

@command
def quit():
    print("QUIT")
    con.stop()

if __name__ == '__main__':
    con = reptyle.Console()
    con.run()