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


class TestCommandMethods(unittest.TestCase):

    def setUp(self):
        # Destroy old root
        if hasattr(context.root, "childs"):
            delattr(context.root, "childs")

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


        exception_raised = False
        @command
        def test():
            pass
        try:
            context.exec("testa")
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

    def test_commands_can_be_called_as_functions(self):
        @command
        def foo():
            foo.has_been_called = True

        @command(parent = foo)
        def bar():
            bar.has_been_called = True

        foo()
        bar()
        self.assertTrue(hasattr(foo, "has_been_called"))
        self.assertTrue(hasattr(bar, "has_been_called"))

    def test_context_dump_tree(self):
        @command
        def foo():
            pass

        @command(parent = foo)
        def bar():
            pass

        @command(parent=foo)
        def baz():
            pass

        @command()
        def bar():
            pass

        expected_tree = """foo
  bar
  baz
bar
"""
        dump = context.dump_tree()
        self.assertEqual(expected_tree, dump)

    def test_named_commands(self):
        @command(name = "foo")
        def bar():
            bar.has_been_called = True

        self.assertTrue("foo" in context.commands())
        self.assertFalse("bar" in context.commands())

        context.exec("foo")
        self.assertTrue(hasattr(bar, "has_been_called"))

    def test_named_parent(self):
        @command(name = "baz")
        def foo():
            foo.has_been_called = True

        @command(parent = foo)
        def bar():
            bar.has_been_called = True

        context.exec("baz bar")
        self.assertFalse(hasattr(foo, "has_been_called"))
        self.assertTrue(hasattr(bar, "has_been_called"))

    def test_multi_level_hierarchy(self):
        @command
        def foo():
            foo.has_been_called = True

        @command(parent=foo)
        def bar():
            bar.has_been_called = True

        @command(parent=bar)
        def baz():
            baz.has_been_called = True

        context.exec("foo bar baz")
        self.assertFalse(hasattr(foo, "has_been_called"))
        self.assertFalse(hasattr(bar, "has_been_called"))
        self.assertTrue(hasattr(baz, "has_been_called"))

    def test_registering_commands_with_same_name_should_yield_an_exception(self):
        @command
        def foo():
            pass

        has_raised_exception = False
        try:
            @command(name = "foo")
            def bar():
                pass
        except exception.GeneralException as e:
            has_raised_exception = True
        self.assertTrue(has_raised_exception)


if __name__ == '__main__':
    unittest.main()