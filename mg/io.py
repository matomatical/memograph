import re
import sys

from prompt_toolkit import prompt as _prompt, print_formatted_text
from prompt_toolkit.formatted_text import HTML

_print = print
_input = input
htmltag = re.compile(r"</?\w+>")

if sys.stdout.isatty():
    def print(*args, **kwargs):
        print_formatted_text(*[HTML(str(s)) for s in args], **kwargs)
else:
    def print(*args, **kwargs):
        _print(*[htmltag.sub("", s) for s in args], **kwargs)

if sys.stdin.isatty():
    def input(prompt, r=None):
        return _prompt(prompt + " ", rprompt=r)
else:
    def input(prompt, r=None):
        if r is not None:
            print(r)
        return _input(prompt + " ")

