from prompt_toolkit import prompt
from typing import Callable, Iterable, List, Union
from prompt_toolkit.completion import CompleteEvent, Completer, Completion
from prompt_toolkit.document import Document
import reptyle.context as context


class CmdCompleter(Completer):
    def __init__(self, words: Union[List[str], Callable[[], List[str]]]):
        self.words = words

    def get_completions(self, document: Document, complete_event: CompleteEvent) -> Iterable[Completion]:
        words = context._commands.keys()
        text_before_cursor = document.text_before_cursor.split(" ")
        word_before_cursor = ""
        if len(text_before_cursor) == 1:
            #Still at toplevel command
            word_before_cursor = text_before_cursor[0].lower()
        else:
            # Get child commands
            child_cmd = context._commands[text_before_cursor[0]].childs
            for cmd in text_before_cursor[1:-1]:
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

class Console:
    def __init__(self):
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            text = prompt('> ', completer=cmd_completer).split(" ")
            cmd = context.exec(text[0], text[1:])
            for word in text[1:]:
                if len(cmd.childs) is 0:
                    break
                cmd = cmd.childs[word]
            cmd()

    def stop(self):
        self.running = False