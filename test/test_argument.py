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