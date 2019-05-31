
from reptyle import context
import lazy_import
import unittest
from unittest.mock import Mock
from reptyle.context import root


class TestArgumentMethods(unittest.TestCase):
	def test_quit(self):
		# Need to lazyimport this module size previous testcases
		# might have destroyed root() during their tearDown
		q = lazy_import.lazy_module("reptyle.builtins.quit")
		# Test command exists
		self.assertTrue(q.quit.__name__ in root.childs)
		self.assertEqual(q.quit, root.childs["quit"])

		# Test to call it via CLI call
		context.quit = Mock()
		context.exec("quit")

		# Test to call it as a function
		context.quit = Mock()
		q.quit()
		context.quit.assert_called()



if __name__ == '__main__':	
	unittest.main()