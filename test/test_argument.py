from reptyle import command, argument, context, exception
import unittest


class TestArgumentMethods(unittest.TestCase):

    def setUp(self):
        # Destroy old root
        if hasattr(context.root, "childs"):
            delattr(context.root, "childs")

    def test_basic_argument(self):
    	@command
    	@argument("arg")
    	def foo(arg):
    		foo.passed_arg = arg

    	context.exec("foo arrrrg")
    	self.assertTrue(hasattr(foo, "passed_arg"))
    	self.assertEqual("arrrrg", foo.passed_arg)

    def test_argument_names_does_not_match(self):
    	exception_raised = False
    	try:
    		@command
    		@argument("arg")
    		def foo(args):
    			pass
    	except exception.GeneralException:
    		exception_raised = True    		
    	self.assertTrue(exception_raised)

    	exception_raised = False
    	try:
    		@command
    		@argument("arg")
    		def foo():
    			pass
    	except exception.GeneralException:
    		exception_raised = True
    	self.assertTrue(exception_raised)

    def test_command_called_with_non_registered_arguments(self):
    	exception_raised = False
    	try:
    		@command
    		def foo(arg):
    			pass
    	except exception.GeneralException:
    		exception_raised = True
    	self.assertTrue(exception_raised)

    def test_command_called_with_too_many_arguments(self):
    	@command
    	@argument("arg")
    	def foo(arg):
    		foo.passed_arg = arg
    	exception_raised = False
    	try:
    		context.exec("foo arrrrg fiz")
    	except exception.ParserException:
    		exception_raised = True
    	self.assertTrue(exception_raised)

    def test_command_with_multiple_arguments(self):
    	@command
    	@argument("arg1")
    	@argument("arg2")
    	def foo(arg1, arg2):
    		foo.passed_arg = [arg1, arg2]


    	context.exec("foo bar baz")
    	self.assertTrue("bar" in foo.passed_arg)
    	self.assertTrue("baz" in foo.passed_arg)

    def test_command_with_description(self):
    	@command
    	@argument("arg", description="a simple argument")
    	def foo(arg):
    		foo.passed_arg = arg
    	self.assertEqual(foo.arguments["arg"]["description"], "a simple argument")

    def test_command_with_flags(self):
    	verb = False
    	@command
    	@argument("verbose", opt="v")   
    	def foo(verbose=False):
    		nonlocal verb
    		verb = verbose
    	context.exec("foo -v")
    	self.assertTrue(verb, "Short flagnames does not work")

    	verb = False
    	context.exec("foo --verbose")
    	self.assertTrue(verb, "Long flagnames does not work")
