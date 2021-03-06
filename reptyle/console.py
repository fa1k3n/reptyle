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

from prompt_toolkit import prompt, history
from prompt_toolkit.shortcuts import CompleteStyle
from typing import Callable, Iterable, List, Union
from prompt_toolkit.completion import CompleteEvent, Completer, Completion
from prompt_toolkit.document import Document
import reptyle.context as context
import reptyle.exception as exception

class CmdCompleter(Completer):
    def __init__(self, words: Union[List[str], Callable[[], List[str]]]):
        self.words = words

    def get_completions(self, document: Document, complete_event: CompleteEvent) -> Iterable[Completion]:
        words = context.commands(context.root)
        text_before_cursor = document.text_before_cursor.split(" ")
        word_before_cursor = ""
        if len(text_before_cursor) == 1:
            #Still at toplevel command
            word_before_cursor = text_before_cursor[0].lower()
        else:
            # Get child commands

            child_cmd = context.root.childs[text_before_cursor[0]].childs
            for cmd in text_before_cursor[1:-1]:
                if cmd in child_cmd and hasattr(child_cmd[cmd], "childs"):
                    child_cmd = child_cmd[cmd].childs
            words = child_cmd.keys()
#

        def word_matches(word: str) -> bool:
            word = word.lower()
            return word.startswith(word_before_cursor)

        for a in words:
            if word_matches(a):
                yield Completion(a, -len(word_before_cursor), None)


cmd_completer = CmdCompleter([])

running = False

def basic_prompt():
    return '> '

class Console:
    def __init__(self, prompt_generator=basic_prompt):
        self._running = False
        self._prompt_generator = prompt_generator
        context.active_con = self

    def run(self):
        self.running = True
        while self.running:
            try:
                text = prompt(self._prompt_generator,
                              completer=cmd_completer,
                              history=history.FileHistory('.reptyle.hist'),
                              complete_style=CompleteStyle.READLINE_LIKE)
                context.exec(text)
            except exception.ParserException as e:
                print(f"ERROR {e}")
            except KeyboardInterrupt:
                self.stop()

    @property
    def running(self):
        return self._running

    @running.setter
    def running(self, val):
        self._running = val

    def print(self, str):
        print(str)

    def stop(self):
        self.running = False