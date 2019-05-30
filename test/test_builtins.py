
from reptyle import command
from reptyle import context as con
from reptyle.builtins import quit as q
import unittest
from unittest.mock import Mock
from reptyle.context import root


class TestArgumentMethods(unittest.TestCase):
	def setUp(self):
	    # Destroy old root
	    if hasattr(con.root, "childs"):
	        delattr(con.root, "childs")

	def test_quit(self):
		con.quit = Mock()
		q.quit()
		con.quit.assert_called()


if __name__ == '__main__':	
	unittest.main()