[![Build status](https://travis-ci.org/fa1k3n/reptyle.svg?branch=master)](https://travis-ci.org/fa1k3n/reptyle)
[![Coverage](https://codecov.io/gh/fa1k3n/reptyle/branch/master/graph/badge.svg)](https://codecov.io/github/fa1k3n/reptyle)
# reptyle 

reptyle is an very lightweight and fast to use REPL style CLI runner build on top of the awesome prompt_toolkit. 

### Getting started

The easiest example of this is 

    import reptyle
    from reptyle.builtins.quit import quit
    
    if __name__ == '__main__':
        con = reptyle.Console()
        con.run()
        
This will give a console with one defines command, quit, which simply quits the console

    > quit
    
### Commands
To create a custom command simply decorate a funtion with @command

    @command
    def foo():
        pass
 
 above will create a command `foo` . A command hierarchy is build using the `parent`
 argument to command
 
     @command
     def foo():
         pass
         
     @command(parent=foo)
     def bar():
         pass
         
 will create the command `foo` and `foo bar` 
 
A command can be given a different name than the function name

    @command(name="baz")
    def foo():
        pass   

will generate the command `baz` only.

### Arguments
A command can have arguments, if so they should be enumerated 
with the @argument declaration during command creation

    @command
    @argument("arg1")
    @argument("arg2")
    def foo(arg1, arg2):
        pass
        
when running the following is accepted, nothing more, nothing less

    > foo arg1 arg2
    
arguments can have optional short flags, for that to work the variable
need to have a default value associated with it

    @command
    @argument("verbose", opt="v")
    @argument("num", "n")
    @argument("arg")
    def foo(arg, verbose=False, num=3):
        pass
        
this allows for the following when running

    > foo -v -n 4 the_arg
    > foo --verbose --num 2 the_arg
    
so both short named with one - and long with -- works

### Future features
* Help command
* More buildins (alias, help, script)
* Colored output control