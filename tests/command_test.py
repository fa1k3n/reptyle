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

from reptyle import command, context, exception
import unittest

class TestStringMethods(unittest.TestCase):
    def test_creation(self):
        @command
        def test():
            test.has_been_called = True

        self.assertTrue("test" in context.commands())
        context.exec("test")
        self.assertTrue(hasattr(test, "has_been_called"))

    def test_unknown_command(self):
        exception_raised = False
        try:
            context.exec("unknown")
        except exception.ParserException:
            exception_raised = True

        self.assertTrue(exception_raised)

    def test_parent_command(self):
        @command
        def foo():
            foo.has_been_called = True

        @command(parent = foo)
        def bar():
            bar.has_been_called = True

        self.assertTrue("foo" in context.commands())
        self.assertFalse("bar" in context.commands())

        # Make sure only bar has been called
        context.exec("foo bar")
        self.assertFalse(hasattr(foo, "has_been_called"))
        self.assertTrue(hasattr(bar, "has_been_called"))

        # And that it still is possible to call foo
        context.exec("foo")
        self.assertTrue(hasattr(foo, "has_been_called"))

    #def test_commands_can_be_called_as_functions(self):
    #    @command
    #    def foo():
    #        foo.has_been_called = True

     #   foo()
     #   self.assertTrue(hasattr(foo, "has_been_called"))

if __name__ == '__main__':
    unittest.main()