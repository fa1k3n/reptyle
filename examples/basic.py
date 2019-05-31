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

from reptyle import command, argument, context
import reptyle.builtins.quit


@command
def foo():
    context.console().print("FOO")

@command(parent=foo)
@argument("fiz")
@argument("verbose", opt="v")
def bar(fiz, verbose=False):
    out = "BAR called"
    if verbose:
        out += " verbosely"
    context.console().print(f"{out} with arg {fiz}")


@command(parent=foo)
@argument("num", opt="n")
def baz(num=3):
    context.console().print(f"BAZ called with num {num}")


if __name__ == '__main__':
    con = reptyle.Console(prompt_generator=lambda: '# ')
    con.run()
    context.console().print("Bye bye!")